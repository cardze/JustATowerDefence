# Codebase Documentation (5 Chapters)

## Chapter 1 — Architecture & Module Map
The project is a small, single-process Pygame application organized into a domain-oriented `tower_defence` package.

**Core modules**
- Runtime entry point: [main.py](../main.py)
- Game state & logic: [tower_defence/app/game.py](../tower_defence/app/game.py)
- Runtime UI loop: [tower_defence/app/main.py](../tower_defence/app/main.py)
- Entities: [tower_defence/entities/enemy.py](../tower_defence/entities/enemy.py), [tower_defence/towers/tower.py](../tower_defence/towers/tower.py), [tower_defence/entities/projectile.py](../tower_defence/entities/projectile.py)
- Configuration constants: [tower_defence/core/config.py](../tower_defence/core/config.py)
- Support systems: [tower_defence/systems/event_system.py](../tower_defence/systems/event_system.py), [tower_defence/combat/attack_strategy.py](../tower_defence/combat/attack_strategy.py), [tower_defence/towers/tower_builder.py](../tower_defence/towers/tower_builder.py), [tower_defence/towers/tower_state.py](../tower_defence/towers/tower_state.py)
- Tests: [test_game.py](../test_game.py)

**High-level flow**
1. [main.py](../main.py) forwards to [tower_defence/app/main.py](../tower_defence/app/main.py), which initializes Pygame and starts the game loop.
2. `Game` in [tower_defence/app/game.py](../tower_defence/app/game.py) owns state (money, lives, wave, entities, speed).
3. Each frame: update state, then render scene + UI.

## Chapter 2 — Game State & Wave Lifecycle
The `Game` class is the authoritative state manager.

**Key state**
- Economy: `money`, `lives`
- Progression: `wave_number`, `wave_in_progress`, `enemies_to_spawn`
- Entities: `enemies`, `towers`, `projectiles`
- Speed scaling: `speed_multiplier`, `enemies_killed`
- Selection: `selected_tower`, `selected_tower_type`

**Wave lifecycle**
- `start_wave()` increments wave and schedules spawns.
- `spawn_enemy()` creates enemies according to `_get_enemy_type_for_wave()`.
- `update()` advances enemies, towers, and projectiles; resolves kills/escapes; ends the wave when all enemies are cleared.
- `generate_complex_path()` changes path every 5 waves.

**Speed scaling**
- `speed_multiplier` increases by `SPEED_INCREASE_PER_KILL` until `MAX_SPEED_MULTIPLIER`.
- `Game.get_current_fps()` scales FPS to make the whole game faster (not just enemies).

## Chapter 3 — Entities: Enemies, Towers, Projectiles
The game entities are simple classes that encapsulate behavior and rendering.

**Enemies** ([tower_defence/entities/enemy.py](../tower_defence/entities/enemy.py))
- Move along a path in `move()`.
- Health scales with wave number.
- `take_damage()` returns whether the enemy died.

**Towers** ([tower_defence/towers/tower.py](../tower_defence/towers/tower.py))
- Config-driven stats from `TOWER_TYPES`.
- Target selection in `find_target()`.
- `update()` fires a `Projectile` when ready.
- `upgrade()` increases damage/range and improves fire rate.

**Projectiles** ([tower_defence/entities/projectile.py](../tower_defence/entities/projectile.py))
- Track a target until hit or target is gone.
- Apply damage on hit; optional AoE for cannon towers.

## Chapter 4 — UI, Input, and Rendering
The UI is built directly in Pygame inside [tower_defence/app/main.py](../tower_defence/app/main.py).

**Rendering**
- `Game.draw()` renders the path, towers, enemies, and projectiles.
- `UI.draw_sidebar()` renders HUD, buttons, and tower selection.
- `UI.draw_game_over()` overlays the game-over screen.

**Input handling**
- Left click in game area: place tower or select an existing tower.
- Left click in sidebar: select tower type or start wave.
- Right click: select a tower to show upgrade/sell actions.

**Interaction helpers**
- Floating upgrade/sell buttons are positioned near the selected tower.
- Click hit-testing uses stored `pygame.Rect` instances.

## Chapter 5 — Configuration, Testing, and Logging
Supporting modules keep gameplay flexible and verifiable.

**Configuration** ([tower_defence/core/config.py](../tower_defence/core/config.py))
- Constants for screen size, FPS, colors, economics, wave rules.
- `TOWER_TYPES` and `ENEMY_TYPES` define gameplay balance.

**Testing** ([test_game.py](../test_game.py))
- Lightweight headless tests for key mechanics:
  - Enemy creation/movement/damage
  - Tower placement/targeting/upgrades
  - Game initialization/wave start/update

**Logging**
- Logging configured in [main.py](../main.py) to file + console.
- Game events are written to `tower_defence.log` in the repo root.
