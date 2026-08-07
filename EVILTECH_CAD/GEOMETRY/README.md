# Geometry Kernel

The geometry package now provides point, vector, curve, surface, topology,
mesh, and solid primitives suitable for deterministic headless CAD workflows.
The lightweight `Mesh` and `Solid` types intentionally favor serializable,
testable behavior over a heavyweight boundary-representation kernel.
