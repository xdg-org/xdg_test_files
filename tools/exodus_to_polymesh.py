#!/usr/bin/env python3
"""Convert an Exodus mesh into an OpenFOAM polyMesh directory.

This exists so that the OpenFOAM cross-check tests can run over geometry that
is identical to what the other backends are given, rather than over a mesh
that merely resembles it. The route is

    .exo --(meshio)--> legacy ASCII .vtk --(vtkUnstructuredToFoam)--> polyMesh

which preserves point coordinates: meshio writes full repr precision and
OpenFOAM writes the result at 17 significant digits, the precision a double
needs to round-trip. The meshes converted here match their source exactly, or
in a rare coordinate to within one unit in the last place (about 1e-16).

Only linear tetrahedra and hexahedra are converted, as those are what XDG
supports. Any other volumetric element block stops the conversion with an
error rather than leaving a hole in the mesh; surface and line blocks are
skipped. Exodus sidesets are not converted: vtkUnstructuredToFoam puts every
boundary face in a single patch, defaultFaces.

Binary VTK is not usable here -- OpenFOAM's vtkUnstructuredReader rejects it --
so the intermediate is always ASCII.

Requires meshio, and netCDF4 for meshio to read Exodus files, plus a sourced
OpenFOAM environment:

    pip install meshio netCDF4
    source /usr/lib/openfoam/openfoam2506/etc/bashrc
    python3 exodus_to_polymesh.py regularized_hex_mesh.exo ../polymesh-regularized-hex
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# the cell types XDG supports
SUPPORTED = {"hexahedron", "tetra"}

# cell types with no volume, which an Exodus file may carry alongside the
# volumetric blocks and which are safe to skip
NON_VOLUMETRIC = {"vertex", "line", "line3", "triangle", "triangle6", "triangle7",
                  "quad", "quad8", "quad9"}

CONTROL_DICT = """FoamFile {{ version 2.0; format ascii; class dictionary; object controlDict; }}
application     none;
startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         1;
deltaT          1;
writeControl    timeStep;
writeInterval   1;
writeFormat     {fmt};
writePrecision  17;
"""

FV_SCHEMES = """FoamFile { version 2.0; format ascii; class dictionary; object fvSchemes; }
ddtSchemes      { default steadyState; }
gradSchemes     { default Gauss linear; }
divSchemes      { default none; }
laplacianSchemes { default Gauss linear corrected; }
"""

FV_SOLUTION = """FoamFile { version 2.0; format ascii; class dictionary; object fvSolution; }
solvers {}
"""


def convert(source: Path, destination: Path, binary: bool,
            zones: bool = False) -> None:
    try:
        import meshio
        import netCDF4  # noqa: F401  needed by meshio's Exodus reader
    except ImportError as err:
        sys.exit(f"{err.name or err} is not installed: pip install meshio netCDF4")

    if shutil.which("vtkUnstructuredToFoam") is None:
        sys.exit("vtkUnstructuredToFoam not found. Source an OpenFOAM environment first.")

    mesh = meshio.read(source)

    unsupported = {b.type: len(b.data) for b in mesh.cells
                   if b.type not in SUPPORTED and b.type not in NON_VOLUMETRIC}
    if unsupported:
        sys.exit(f"{source} has volumetric element blocks XDG does not support: "
                 f"{unsupported}. Only linear tetrahedra and hexahedra are converted.")

    # names are paired with blocks before any are skipped, so that skipping a
    # surface block cannot shift the names of the blocks after it
    names = block_names(source, len(mesh.cells))
    kept = [(name, block) for name, block in zip(names, mesh.cells)
            if block.type in SUPPORTED]
    if not kept:
        sys.exit(f"{source} contains no tetrahedra or hexahedra")
    cells = [block for _, block in kept]

    skipped = {b.type: len(b.data) for b in mesh.cells if b.type in NON_VOLUMETRIC}
    if skipped:
        print(f"  skipping surface and line element blocks: {skipped}")
    if side_set_count(source):
        print("  note: Exodus sidesets are not converted; every boundary face "
              "goes into one patch, defaultFaces")

    total = sum(len(block.data) for block in cells)
    print(f"  {source.name}: {len(mesh.points)} points, {total} cells "
          f"in {len(cells)} block(s)")

    with tempfile.TemporaryDirectory() as scratch:
        case = Path(scratch)
        (case / "system").mkdir()
        fmt = "binary" if binary else "ascii"
        (case / "system" / "controlDict").write_text(CONTROL_DICT.format(fmt=fmt))
        (case / "system" / "fvSchemes").write_text(FV_SCHEMES)
        (case / "system" / "fvSolution").write_text(FV_SOLUTION)

        vtk = case / "mesh.vtk"
        meshio.write(vtk, meshio.Mesh(mesh.points, cells), binary=False)

        subprocess.run(["vtkUnstructuredToFoam", vtk.name],
                       cwd=case, check=True, stdout=subprocess.DEVNULL)
        if binary:
            subprocess.run(["foamFormatConvert"],
                           cwd=case, check=True, stdout=subprocess.DEVNULL)

        report = subprocess.run(["checkMesh"], cwd=case,
                                capture_output=True, text=True)
        if report.returncode != 0 or "Mesh OK" not in report.stdout:
            tail = "\n".join((report.stdout + report.stderr).splitlines()[-15:])
            sys.exit(f"checkMesh did not report a valid mesh for {source}:\n{tail}")

        poly = case / "constant" / "polyMesh"
        if destination.exists():
            shutil.rmtree(destination)
        # checkMesh drops a sets/ directory in the mesh; it is diagnostic output
        # rather than part of the mesh, so it is not carried over
        shutil.copytree(poly, destination,
                        ignore=shutil.ignore_patterns("sets"))

        if zones:
            write_cell_zones(destination, cells, [name for name, _ in kept])

    written = sorted(p.name for p in destination.iterdir())
    size = sum(p.stat().st_size for p in destination.iterdir())
    print(f"  -> {destination}  [{', '.join(written)}]  {size / 1024:.0f} KiB, checkMesh OK")


def block_names(source: Path, count: int) -> list:
    """Names for the Exodus element blocks, with Block_<id> for any left unnamed.

    <id> is the block's Exodus ID (eb_prop1), as Exodus tools show it, or its
    position when the file carries no IDs.
    """
    names = [""] * count
    ids = list(range(1, count + 1))
    try:
        import netCDF4
    except ImportError:
        return [f"Block_{i}" for i in ids]
    try:
        with netCDF4.Dataset(source) as nc:
            raw = nc.variables.get("eb_names")
            if raw is not None:
                read = [str(s).strip() for s in netCDF4.chartostring(raw[:])]
                names = (read + names)[:count]
            prop = nc.variables.get("eb_prop1")
            if prop is not None and len(prop) == count:
                ids = [int(v) for v in prop[:]]
    except OSError as err:
        print(f"  note: could not read block names from {source}: {err}")
    return [name or f"Block_{i}" for name, i in zip(names, ids)]


def side_set_count(source: Path) -> int:
    """Number of sidesets in the Exodus file, or 0 if it cannot be read."""
    try:
        import netCDF4
        with netCDF4.Dataset(source) as nc:
            dim = nc.dimensions.get("num_side_sets")
            return len(dim) if dim is not None else 0
    except Exception:
        return 0


def write_cell_zones(destination: Path, cells, names) -> None:
    """Write one cellZone per element block.

    vtkUnstructuredToFoam keeps cells in the order they appear in the VTK file,
    and the blocks are written there consecutively, so each block occupies a
    contiguous run of cell indices. That is what makes the ranges below valid,
    and it is worth re-checking against cell centroids if the conversion route
    ever changes.
    """
    header = """FoamFile
{{
    version     2.0;
    format      ascii;
    class       regIOobject;
    location    "constant/polyMesh";
    object      cellZones;
}}

{n}
(
"""
    with open(destination / "cellZones", "w") as out:
        out.write(header.format(n=len(cells)))
        start = 0
        for name, block in zip(names, cells):
            stop = start + len(block.data)
            out.write(f"{name}\n{{\n    type            cellZone;\n"
                      f"    cellLabels      List<label> {stop - start}\n(\n")
            # written in chunks: a single join over a few million labels is
            # needlessly hard on memory
            for lo in range(start, stop, 100_000):
                out.write("\n".join(map(str, range(lo, min(lo + 100_000, stop)))))
                out.write("\n")
            out.write(")\n;\n}\n")
            print(f"    zone {name}: cells {start}..{stop - 1}")
            start = stop
        out.write(")\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path, help="input Exodus (.exo) mesh")
    parser.add_argument("destination", type=Path, help="polyMesh directory to write")
    parser.add_argument("--binary", action="store_true",
                        help="write a binary polyMesh, which is smaller and "
                             "exercises the faceCompactList reader path")
    parser.add_argument("--zones", action="store_true",
                        help="write a cellZone per Exodus element block, so that "
                             "the blocks survive as XDG volumes and materials")
    args = parser.parse_args()
    convert(args.source, args.destination, args.binary, args.zones)


if __name__ == "__main__":
    main()
