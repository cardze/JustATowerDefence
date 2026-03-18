## ADDED Requirements

### Requirement: 3D enemy scene with track-based movement
The system SHALL render enemies as 3D models (spheres) that move along predefined waypoint tracks through 3D space.

#### Scenario: Enemy spawns at track start
- **WHEN** a wave spawns an enemy
- **THEN** the enemy appears at the track's starting waypoint position (X, Y, Z)

#### Scenario: Enemy moves along track
- **WHEN** an enemy is active and time progresses
- **THEN** the enemy moves smoothly along the track from waypoint to waypoint at a constant speed

#### Scenario: Enemy reaches track end
- **WHEN** an enemy reaches the final waypoint of the track
- **THEN** the enemy despawns or triggers a game event (life lost, score update)

### Requirement: Enemy health and damage visualization
The system SHALL track enemy health and provide visual feedback when an enemy takes damage.

#### Scenario: Enemy health depletes on hit
- **WHEN** a projectile hits an enemy
- **THEN** enemy health decreases by projectile damage value

#### Scenario: Health bar displayed over enemy
- **WHEN** an enemy has taken damage or is selected
- **THEN** a health bar appears above the enemy showing current health / max health

#### Scenario: Enemy dies when health reaches zero
- **WHEN** an enemy's health reaches 0
- **THEN** the enemy plays a death animation and is removed from the world

### Requirement: Enemy visual state and animation
The system SHALL animate enemies to show movement along tracks and provide death feedback.

#### Scenario: Enemy rotation follows track direction
- **WHEN** an enemy moves along a track
- **THEN** the enemy's facing direction (rotation) smoothly orients toward the current waypoint

#### Scenario: Enemy death animation plays
- **WHEN** an enemy health reaches 0
- **THEN** a brief animation plays (e.g., scale down, fade, explosion particle) before removal

### Requirement: Multiple enemies in world
The system SHALL support spawning and managing many enemies simultaneously with independent state and movement.

#### Scenario: Wave spawns multiple enemies
- **WHEN** a wave is triggered with a spawn count of 10
- **THEN** 10 distinct enemy nodes are created and all move along the track independently

#### Scenario: Different enemy types with different speeds
- **WHEN** a wave spawns enemies of different types (e.g., fast and slow)
- **THEN** each type moves at its configured speed along the same track

### Requirement: Enemy-tower interaction detection
The system SHALL determine when enemies are in range of towers for targeting and attack purposes.

#### Scenario: Tower detects enemy in range
- **WHEN** an enemy moves within a tower's range sphere
- **THEN** the tower can target and attack the enemy

#### Scenario: Tower loses track of enemy
- **WHEN** an enemy exits a tower's range
- **THEN** the tower stops targeting that enemy and returns to idle state
