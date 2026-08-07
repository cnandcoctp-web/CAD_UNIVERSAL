# User Interface Framework

The EvilTech CAD UI module provides a headless, testable interface framework
for engineering workflows. It integrates with the locked Foundation,
Mathematical Engine, Geometry Kernel, and Rendering Engine packages without
implementing their responsibilities.

Implemented capabilities:

- Application window, home screen, project dashboard, and main workspace
- Menu bar, ribbon toolbar, and quick access toolbar
- Status, notification, progress, task, and simulation-status surfaces
- Docking framework and workspace layout management
- Project explorer, object tree, properties panel, inspector panel
- Layer manager, material browser, asset browser, and command console
- UI viewport management and viewport controls
- Theme manager with light and dark themes
- Keyboard shortcut and mouse input managers
- Recent projects, project wizard, open/save dialogs, about, help, and settings

Not implemented here:

- Native OS windows, actual GUI toolkit bindings, and drag-and-drop docking backends
- Project persistence logic, simulation execution, modeling tools, AI, or engineering-domain modules

Those capabilities remain owned by their respective construction packages and are
documented rather than implemented in this module.
