# Rendering Engine

The EvilTech CAD rendering engine provides a headless, testable visualization
pipeline that integrates with the locked Foundation, Mathematical Engine, and
Geometry Kernel layers.

Implemented capabilities:

- Rendering context and render loop
- Scene graph and scene manager
- Perspective and orthographic cameras
- Camera controller with zoom, pan, orbit, and rotate
- Viewport manager with multi-viewport support
- Render pipeline and renderer
- Grid and axis frame descriptors
- Lighting, materials, textures, and shaders management
- Overlay rendering, coordinate gizmo, and background system
- Bounding-box overlays and object picking

Out-of-scope features such as UI windows, GPU backends, and modeling-specific
render workflows remain in their owning packages and are documented rather than
implemented here.
