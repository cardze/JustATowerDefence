## 1. Project Setup & Infrastructure

- [x] 1.1 Initialize Godot 4 project with folder structure (scenes/, scripts/, assets/, levels/)
- [x] 1.2 Create base scene hierarchy (Main.tscn as root, with Level scene as child)
- [x] 1.3 Create GameManager autoload script and register in project settings
- [x] 1.4 Set up Godot project.godot with target resolution (1920x1080), physics (3D), and rendering settings

## 2. Rendering Engine & Camera

- [ ] 2.1 Create 3D world environment with DirectionalLight3D and WorldEnvironment
- [ ] 2.2 Implement Camera3D with isometric position and orientation (45° angle)
- [ ] 2.3 Add pan camera control (arrow keys/WASD move camera left/right/forward/back)
- [ ] 2.4 Add zoom camera control (mouse scroll wheel adjusts distance/FOV)
- [ ] 2.5 Implement camera bounds to prevent panning beyond level edges
- [ ] 2.6 Create camera raycast system to convert mouse clicks to 3D world positions
- [ ] 2.7 Set up materials for towers (blue), enemies (red), projectiles (yellow), and terrain (gray)

## 3. Terrain & Level Foundation

- [ ] 3.1 Create flat terrain plane (CSGBox3D or MeshInstance3D) as ground base
- [ ] 3.2 Design and implement track waypoint system (array of Vector3 positions)
- [ ] 3.3 Create track visualization in editor (draw line between waypoints)
- [ ] 3.4 Implement track follower logic (enemy position = Lerp between waypoints based on time)
- [ ] 3.5 Create Level.tscn scene with terrain, track nodes, and lighting setup

## 4. Enemy System

- [ ] 4.1 Create Enemy.tscn scene with SphereMesh, CollisionShape3D, and Enemy.gd script
- [ ] 4.2 Implement enemy properties (health, speed, reward, track reference)
- [ ] 4.3 Implement enemy movement along track waypoints (update position each frame)
- [ ] 4.4 Add health depletion logic and death state
- [ ] 4.5 Create enemy death animation and signal emission
- [ ] 4.6 Implement health bar display above enemy (ProgressBar3D or Canvas label)
- [ ] 4.7 Create EnemyManager in GameManager to spawn and track all active enemies
- [ ] 4.8 Implement wave spawning (create N enemies at track start at intervals)

## 5. Tower System

- [ ] 5.1 Create Tower.tscn scene with CylinderMesh, CollisionShape3D, and Tower.gd script
- [ ] 5.2 Implement tower properties (position, cost, range, damage, cooldown, level)
- [ ] 5.3 Implement tower placement validation (cost check, overlap check, terrain check)
- [ ] 5.4 Implement tower targeting (find nearest enemy in range)
- [ ] 5.5 Implement firing logic (create projectile when cooldown expired and target exists)
- [ ] 5.6 Create tower range visualization (sphere outline or wireframe)
- [ ] 5.7 Add tower state feedback visual (color change when targeting)
- [ ] 5.8 Create TowerManager in GameManager to spawn and track all towers
- [ ] 5.9 Implement tower placement preview (semitransparent preview at mouse position)
- [ ] 5.10 Add tower preview validation feedback (red/green for invalid/valid placement)

## 6. Projectile System

- [ ] 6.1 Create Projectile.tscn scene with SphereMesh (small) and Projectile.gd script
- [ ] 6.2 Implement projectile movement toward target (straight line from tower to enemy)
- [ ] 6.3 Implement projectile-enemy collision detection (distance check each frame)
- [ ] 6.4 Implement damage application on hit and projectile removal
- [ ] 6.5 Create projectile visual distinction by tower type (color/size)
- [ ] 6.6 Implement projectile speed and configurable trajectories
- [ ] 6.7 Add projectile lead targeting (aim at predicted enemy position)
- [ ] 6.8 Create impact particle effect or visual feedback on hit
- [ ] 6.9 Create ProjectileManager for spawning and tracking active projectiles

## 7. Game Logic & State Management

- [ ] 7.1 Implement GameManager state properties (money, lives, current_wave, wave_count)
- [ ] 7.2 Create signal system for game events (enemy_died, tower_placed, wave_started, etc.)
- [ ] 7.3 Implement wave progression logic (spawn next wave when all enemies defeated)
- [ ] 7.4 Implement money system (initial money, reward on kill, cost on placement)
- [ ] 7.5 Implement lives system (starts at 20, decreases on enemy escape, game over at 0)
- [ ] 7.6 Create game loop (update enemies, towers, projectiles each frame)
- [ ] 7.7 Implement collision detection between projectiles and enemies
- [ ] 7.8 Implement game over condition and transition to game over screen
- [ ] 7.9 Implement win condition (survive max waves) and victory screen

## 8. User Interface & Input

- [ ] 8.1 Create Input.gd script to handle all input (pan, zoom, click placement)
- [ ] 8.2 Implement tower selection/preview on mouse move
- [ ] 8.3 Implement tower placement on left mouse click (if valid)
- [ ] 8.4 Create HUD canvas with money, lives, wave counter display
- [ ] 8.5 Implement tower stats display on hover/selection
- [ ] 8.6 Create simple game over screen with restart button
- [ ] 8.7 Create simple victory screen with next level/restart option

## 9. Content & Configuration

- [ ] 9.1 Define tower types (BasicTower, FastTower, CannonTower) with stats in constants
- [ ] 9.2 Define enemy types (BasicEnemy, FastEnemy) with stats in constants
- [ ] 9.3 Create wave configuration (wave 1-10, enemies per wave, difficulty scaling)
- [ ] 9.4 Design and create first playable level (track path, terrain, starting money/lives)
- [ ] 9.5 Create tower cost and balance values (cost, damage, range, cooldown)
- [ ] 9.6 Tune enemy speed, health, and rewards for fun pacing

## 10. Testing & Polish

- [ ] 10.1 Manual playtest level (place towers, kill enemies, complete wave)
- [ ] 10.2 Test edge cases (money insufficient, overlapping towers, camera bounds)
- [ ] 10.3 Test game over condition (lose all lives before wave end)
- [ ] 10.4 Test victory condition (survive all waves)
- [ ] 10.5 Test camera pan/zoom responsiveness and bounds
- [ ] 10.6 Test tower range visualization and targeting accuracy
- [ ] 10.7 Fine-tune balance (enemy difficulty, tower cost/power, wave progression)
- [ ] 10.8 Add placeholder audio (shoot sound, hit sound, background music) or document as post-MVP

## 11. Build & Deployment

- [ ] 11.1 Configure Godot project export settings (Windows, macOS, Linux)
- [ ] 11.2 Build and export standalone executable
- [ ] 11.3 Create README with build instructions and gameplay guide
- [ ] 11.4 Test executable on target platforms (or at least generate build artifacts)
