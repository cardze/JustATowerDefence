## Context

Current game is implemented in Python with Pygame 2D rendering. All game logic (towers, enemies, projectiles, waves) lives in modular classes with an event-driven architecture. The codebase has seen refactoring to improve readability and clean code practices.

Migrating to Godot 4 means rewriting the entire system in GDScript using Godot's node/scene architecture, signal system (replaces custom EventManager), and 3D physics/rendering pipeline.

## Goals / Non-Goals

**Goals:**
- Implement Godot 4 project structure with scene-based architecture for towers, enemies, projectiles
- Support 3D rendering with simple geometric primitives (cylinder, sphere, box) for MVP
- Implement track system with 3D waypoint nodes for enemy pathing
- Create GameManager autoload to handle game state, waves, player money
- Support free-form 3D tower placement with visual feedback and range visualization
- Build fixed isometric camera system for player interaction
- Implement tower targeting, projectile physics, and enemy damage/death
- Achieve gameplay parity with 2D version (shoot enemies, spend money, waves progress) in 3D space
- Create at least one complete playable level demonstrating core mechanics

**Non-Goals:**
- Tower upgrades, sell system, multiple difficulty levels (post-MVP)
- Advanced shaders, particle effects, or AAA-grade graphics (post-MVP)
- Multiple levels/campaigns (single MVP level)
- Procedural generation or AI-driven strategy recommendation
- Mobile optimization or WebGL builds (desktop only for MVP)

## Decisions

### 1. **Architecture: Scene-Based vs Module-Based**
**Decision:** Scene-based (Godot nodes). Each entity (Tower, Enemy, Projectile) is a scene (`.tscn` file with attached `.gd` script).

**Rationale:** Godot's scene tree is the intended pattern. Scenes provide composition, inheritance, and visual editing. Aligns with engine idioms vs. forcing 2D Python patterns into 3D space.

**Alternatives considered:**
- Pure GDScript modules (like Python): Less Godot-idiomatic, loses visual scene hierarchy benefits
- Hybrid (scenes + managers): More complex; scenes are sufficient with autoloads

### 2. **Enemy Pathing: Track Nodes vs Pathfinding**
**Decision:** Track-based waypoints. Enemy receives reference to track, moves along waypoint chain at constant speed.

**Rationale:** Simpler implementation (linear interpolation between nodes), predictable behavior, allows designer control over difficulty (dense tracks = hard, sparse tracks = easy). Matches your 3D vision of "rails/tracks."

**Alternatives considered:**
- 3D pathfinding (A*): Overkill for MVP, adds AI complexity, less designer control
- Physics-based (forces/velocity): More realistic but harder to tune wave timing

### 3. **Tower Placement: Free-Form vs Snapped**
**Decision:** Free-form 3D placement. Player clicks in world, tower places at mouse intersection point.

**Rationale:** You specified "towers placeable anywhere in 3D space." Uses Godot raycasting to find click position in 3D world.

**Cost:** Need collision check to prevent overlapping towers; input handling is more complex than grid-based.

### 4. **Game State Management: Autoload Singleton vs Scene-Scoped**
**Decision:** GameManager as autoload singleton (always exists, persistent across scenes).

**Rationale:** Game state (money, waves, entities) needs to be globally accessible. Autoload is cleaner than passing references through every node.

**Risks:** Singletons can become dumping grounds; mitigate by clear responsibility (game state only, not all logic).

### 5. **Event System: Godot Signals vs Custom EventBus**
**Decision:** Use Godot's built-in signal system (replaces Python EventManager).

**Rationale:** Signals are engine-native, connect visually in editor, first-class feature. No need for custom observer pattern.

**Cost:** Less flexible than custom event bus; signals are statically typed to sender's signature. Acceptable for MVP.

### 6. **Camera: Fixed Isometric vs Player-Controlled**
**Decision:** Fixed isometric angle (45°) with pan/zoom controls via mouse/keyboard.

**Rationale:** Keeps implementation simple; classic tower defense camera angle. Pan/zoom allows level exploration without full 360° rotation complexity.

**Alternatives:** Fully rotatable (more modes, more control), First-person (disorienting for tower defense).

### 7. **Rendering: Primitives vs Imported Meshes**
**Decision:** Use Godot primitives (MeshInstance3D with CylinderMesh, SphereMesh, BoxMesh) for MVP.

**Rationale:** Fast iteration, no asset pipeline setup. Can import Blender models post-MVP.

### 8. **Physics: RigidBody3D vs Area3D vs Raycast**
**Decision:** Area3D for tower proximity checks (range visualization). Raycast for targeting and tower placement clicks. No rigid bodies (enemies follow pre-determined tracks).

**Rationale:** Simplest approach. Avoids gravity simulation; enemies move on rails, not via physics.

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| **Learning curve (Godot/GDScript)** | Start with simple scenes, build incrementally. Clear commit messages. Document patterns as we discover them. |
| **Loss of Python codebase patterns** | Archive tower_defence/ as reference. Patterns (Strategy, State, Observer) still apply in Godot; adapt to GDScript idioms. |
| **Track-based pathing feels restrictive** | Design tracks to be interesting and non-obvious. Alternative: post-MVP add waypoint editor for L creators. |
| **Fixed camera limits level expressiveness** | Isometric is proven TD mechanic. Pan/zoom mitigates. Full rotation is post-MVP feature. |
| **3D input (clicking world) adds complexity** | Raycast is straightforward in Godot. Test early. |
| **Primitives look basic** | Acceptable for MVP. Visuals can improve without breaking logic. |

## Migration Plan

No rollback needed (separate codebase from Python version). Deployment:

1. **Development:** Build in Godot Editor, test locally
2. **Packaging:** Export from Godot as standalone executable (Linux/macOS/Windows)
3. **Release:** Share executable + instructions to run

**Fallback:** If MVP scope slips, ship "level editor works, one level playable" as minimal viable state.

## Open Questions

- Should tower range visualization be a sphere mesh overlay or wireframe/debug shape?
- What track shape for MVP (circular, spiral, zigzag)?
- How many tower types for MVP (1 generic, or 2-3 variants)?
- Should enemies all be same speed or mix slow/fast for waves?
- Win condition: kill all enemies in final wave, or reach wave 10?
