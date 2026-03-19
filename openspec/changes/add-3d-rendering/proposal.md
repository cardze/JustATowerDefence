## Why

The current 2D Pygame implementation limits gameplay and visual presentation. Converting to 3D unlocks vertical level design, spatial complexity, and immersive visuals. A 3D tower defense with players placing towers in 3D space and enemies navigating 3D tracks creates richer gameplay moments and opens new strategic possibilities.

## What Changes

- **Complete engine migration** from Pygame 2D to Godot 4 for true 3D rendering
- **New coordinate system**: Towers, enemies, and projectiles operate in 3D space (X, Y, Z)
- **Track-based enemy movement**: Enemies follow predefined 3D path waypoints rather than grid-based movement
- **Free-form tower placement**: Towers placeable anywhere in 3D space (on ground, platforms, suspended, etc.)
- **New game loop architecture**: Godot's scene system replaces Python module-based design
- **3D camera system**: Isometric-style fixed camera with pan/zoom/rotation controls
- **MVP scope**: Single playable level with basic tower types, wave spawning, and core mechanics (no progression/upgrades in initial release)

## Capabilities

### New Capabilities

- `3d-rendering-engine`: Godot 4 scene system, 3D rendering pipeline, lighting, materials, and shader support
- `3d-camera-system`: Fixed isometric camera with pan/zoom/rotation for viewing 3D world
- `3d-tower-visualization`: 3D tower models (primitives initially), placement feedback, tower range visualization
- `3d-enemy-visualization`: 3D enemy models, skeletal animation for movement along tracks, death animation
- `3d-terrain-system`: 3D track definition with waypoint nodes, level loading, terrain collision
- `3d-projectile-visualization`: 3D projectile paths, particle effects on impact, AoE visualization
- `3d-game-logic-adaptation`: Game state machine, tower attack logic, wave spawning system in Godot

### Modified Capabilities

<!-- No existing specs being modified; this is a complete fresh architecture -->

## Impact

- **Codebase**: Complete rewrite; Python tower_defence package archived as reference documentation
- **Dependencies**: Godot 4.x (no longer Pygame); GDScript replaces Python for game logic
- **Testing**: Test suite rebuilt in Godot's testing framework; manual testing during MVP
- **Development**: Requires GDScript/Godot learning; estimated 1-2 weeks for MVP completion
- **Deployment**: Standalone Godot executable builds for Win/Mac/Linux
