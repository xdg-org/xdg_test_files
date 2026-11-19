# Manifest

## single-tet.h5m/exo

A mesh containing a single tetrahedron. In the case of the `.h5m` file, the tet
composes a single volume and each triangle of the tet is it's own surface.

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 4     |
| Tetrahedrons      | 1     |

<div align="center">
  <img src="images/single-tet.png" alt="Single Tetrahedron" width="600">
</div>

The same mesh as above but uniformly refined one time to form a small tet mesh consisting of 8 tetrahedra with the same external nodes mesh containing a single tetrahedron.

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 16    |
| Tetrahedrons      | 8     |

<div align="center">
  <img src="images/small-tet-mesh.png" alt="Small Tetrahedra Mesh" width="600">
</div>

## jezebel.h5m

A simple sphere geometry matching the size of the Jezebel bare sphere core (more info [here](https://www.osti.gov/servlets/purl/1344338)). This file contains a surface mesh only.

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 1276  |
| Tetrahedrons      | 10333 |

## jezebel.exo

A simple sphere geometry matching the size of the Jezebel bare sphere core (more info [here](https://www.osti.gov/servlets/purl/1344338)).
This file contains a tetrahedral mesh.

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 1276  |
| Tetrahedrons      | 10333 |

## no_overlap.h5m
A simple cube and Cylinder geometry with two volumes that do no overlap.

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 1032  |

## no_overlap_imp.h5m
The same as no_overlap.h5m but imprinted?

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 1290  |

## overlap.h5m
A simple Cube and Sphere geometry with two volumes that do overlap.

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 88220 |

## small_overlap.h5m
A simple Cube and Cylinder geometry with two volumes that overlap over a very small region.

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 1032  |

## enclosed.h5m
A simple geometry with two concentric Cylinders - one completely enclosed by the larger one.

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 2040  |

## brick.exo
A 10 x 10 x 10 brick centered on the origin. No additional sidesets. (tet mesh)

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 1404  |
| Tetrahedrons      | 8790  |

## brick-sidesets.exo
A 10 x 10 x 10 brick centered on the origin. Each surface has a sideset. (tet mesh)

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 1404  |
| Tetrahedrons      | 8790  |

## cyl-brick.exo
A 10 x 10 x 10 brick centered on (0, 0, 10) and a cylinder of radius 5 height 10 centered on the origin w/ rotation axis along Z. (tet mesh)

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 2692  |
| Tetrahedrons      | 8790  |

## overlap-edge.h5m
A simple edge overlap case consisting of two identical pyramids which have a volume overlap along a triangle edge (no overlapping vertices).

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 44    |

<div align="center">
  <img src="images/overlap-edge.png" alt="Overlap Edge" width="600">
</div>


## beam-overlaps.h5m
A second edge overlap case consisting of two identical beams (cuboids) which have a larger volume overlap (no vertices) along multiple edges.

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 136   |

<div align="center">
  <img src="images/beam-overlap.png" alt="Beam Overlaps" width="600">
</div>

# pincell.h5m and pincell-implicit.exo

These two files contain identical meshing in MOAB (`.h5m`) and libMesh (`.exo`)
formats. Metadata is applied in the Cubit model (found in `pincell-both.cub5`)
for both formats as well.

## pincell.h5m

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 32544 |


## pincell.exo

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 24912 |
| Tetrahedrons      | 93170 |

<div align="center">
  <img src="images/pincell-geom.png" alt="Pincell problem geometry" width="600">
  <img src="images/pincell-mesh.png" alt="Pincell problem mesh" width="600">
</div>

In the case of the libMesh model, boundary conditions are only applied to the
outer volume. The interior interfaces of the model are discovered automatically
as implicit boundaries based on the transition between mesh blocks.

# segmented-beam.h5m

A simple rectangular beam segmented into 20 seperate volumes along the x-axis.

| Element Type      | Count |
|-------------------|-------|
| Surface Triangles | 1106  |

<div align="center">
  <img src="images/single-segmented-beam.png" alt="Segmented Beam" width="600">
</div>

# cube-mesh-no-geom.exo/h5m/cub5

A simple cube geometry that holds no metadata, only a tet mesh.

<div align="center">
  <img src="images/cube-no-geom.png" alt="Cube mesh without geometry or metadata" width="600">
</div>

## Jezebel-quads

A simple sphere surface mesh composed of quadrilateral elements. This model
matches the dimensions of the tet/tri jezebel files above.

| Element Type   | Count |
|----------------|-------|
| Surface Quads  | 2400  |
| Hexahedra      | 36800 |


<div align="center">
  <img src="images/quad-sphere.png" alt="Jezebel sphere mesh with hexes/quads" width="463">
</div>

## cyl-brick-quads.h5m/exo

A 10 x 10 x 10 brick centered on (0, 0, 14.5) and a cylinder of radius 5 height 15 centered on the origin w/ rotation axis along Z. (hex mesh)

| Element Type   | Count  |
|----------------|--------|
| Surface Quads  | 30478  |
| Hexahedra      | 187200 |

<div align="center">
  <img src="images/cyl-brick-quads.png" alt="Multi-volume model using hexes/quads" width="463">
</div>


## Cube with Multiblock Sideset (cube-w-multiblock-sideset.*)

This test case is added to address https://github.com/xdg-org/xdg/issues/212
specifically. Cubit, MOAB, and Exodus file are provided.

| Element Type   | Count |
|----------------|-------|
| Triangles      | 3234  |
| Tetrahedron    | 13000 |
| Vertices       | 5204  |

<div align="center">
  <img src="images/cube-w-multiblock-sideset-geom.png" alt="Cube with multiblock sideset geom" width="463">
  <img src="images/cube-w-multiblock-sideset-geom.png" alt="Cube with multiblock sideset. Sideset is highlighted" width="463">
</div>

## cyl-brick-quads.h5m/exo

A 10 x 10 x 10 brick centered on (0, 0, 14.5) and a cylinder of radius 5 height 15 centered on the origin w/ rotation axis along Z. (hex mesh)

| Element Type   | Count  |
|----------------|--------|
| Surface Quads  | 30478  |
| Hexahedra      | 187200 |

<div align="center">
  <img src="images/cyl-brick-quads.png" alt="Multi-volume model using hexes/quads" width="463">
</div>

## regularized_tet_mesh.exo/h5m

This is a tet mesh created with tets matching the boundary of a regular/Cartesian mesh 10 elements in each direction x, y, and z and extents from (-10, -10, -10) to (10, 10, 10) in model units. There are 12 tetrahedron per single regularized mesh element.

No geometry metadata is added to this mesh. It is used purely to test element-to-element ray traversal.

| Element Type  | Count |
|---------------|-------|
| Tetrahedron   | 12000 |

<div align="center">
  <img src="images/regularized_tet_mesh.png" alt="Regularized tetrahedral mesh" width="463">
</div>


## regularized_hex_mesh.exo/h5m

This is a tet mesh created with tets matching the boundary of a regular/Cartesian mesh 10 elements in each direction x, y, and z and extents from (-10, -10, -10) to (10, 10, 10) in model units. There is one hexahedral element per regularized mesh element.

No geometry metadata is added to this mesh. It is used purely to test element-to-element ray traversal.

| Element Type  | Count |
|---------------|-------|
| Tetrahedron   | 1000  |

<div align="center">
  <img src="images/regularized_hex_mesh.png" alt="Regularized hexehedral mesh" width="463">
</div>

## four_region_hex.exo/h5m

This is a hex mesh of a four-region geometry segmented into two volumes. Region one extends from
(-0.5, -0.5, -0.25) to (0.5, 0.5, 0.25), region two extends from (-0.5, -0.5, 0.25) to (0.5, 0.5, 0.75),
region three extends from (-0.5, -0.5, 0.75) to (0.5, 0.5, 1.25), and region four extends from
(-0.5, -0.5, 1.25) to (0.5, 0.5, 1.75). Regions one and three are bundled into a single volume (with
an ID of 2), and regions two and four are bundled into a single volume (with an ID of 1). Each
region contains 64 hexahedral elements.

No geometry metadata is added to this mesh. It is used purely to test mesh manager volume inclusion/exclusion.

| Element Type  | Count |
|---------------|-------|
| Hexahedron    | 256   |

<div align="center">
  <img src="images/four_region_hex.png" alt="Four region hexehedral mesh" width="463">
</div>

## amr_mesh_tet.exo

This is a tetrahedral mesh of a two region geometry with elements generated from an adaptive mesh refinement sequence
from within XDG's test suite. As AMR connectivity is not stored in Exodus files, the adapted mesh cannot be
loaded from a file (and so the unadapted mesh is included here).

No geometry metadata is added to this mesh. It is used purely to test element to element ray traversal and find
element calls when an AMR mesh is provided to a libMesh mesh manager.

| Element Type  | Count (no AMR) | Count (with AMR) |
|---------------|----------------|------------------|
| Tetrahedron   |       192      |       6352       |

<div align="center">
  <img src="images/amr_mesh_tet_unrefined.png" alt="Two region TET4 mesh prior to the application of AMR" width="231">
  <img src="images/amr_mesh_tet.png" alt="Two region TET4 mesh after the application of AMR in XDG's test suite" width="231">
</div>

## amr_mesh_hex.exo

This is a hexahedral mesh of a two region geometry with elements generated from an adaptive mesh refinement sequence
from within XDG's test suite. As AMR connectivity is not stored in Exodus files, the adapted mesh cannot be
loaded from a file (and so the unadapted mesh is included here).

No geometry metadata is added to this mesh. It is used purely to test element to element ray traversal and find
element calls when an AMR mesh is provided to a libMesh mesh manager.

| Element Type  | Count (no AMR) | Count (with AMR) |
|---------------|----------------|------------------|
| Hexahedron    |       32       |       1096       |

<div align="center">
  <img src="images/amr_mesh_hex_unrefined.png" alt="Two region HEX8 mesh prior to the application of AMR" width="231">
  <img src="images/amr_mesh_hex.png" alt="Two region HEX8 mesh after the application of AMR in XDG's test suite" width="231">
</div>
