## ADDED Requirements

### Requirement: 3D projectile scene and rendering
The system SHALL instantiate projectiles as 3D objects that travel from tower to enemy position in 3D space.

#### Scenario: Projectile created at tower position
- **WHEN** a tower fires at a target
- **THEN** a projectile object is created at the tower's position in 3D world

#### Scenario: Projectile moves toward enemy
- **WHEN** a projectile is active
- **THEN** the projectile moves in a straight line (or arc) from its creation point toward the enemy's current position

#### Scenario: Projectile despawns on hit or timeout
- **WHEN** a projectile reaches the enemy or time expires
- **THEN** the projectile is removed from the scene

### Requirement: Projectile-enemy collision detection
The system SHALL detect when a projectile reaches or hits an enemy in 3D space and apply damage.

#### Scenario: Projectile hit detection
- **WHEN** a projectile's position comes within a hit radius of an enemy
- **THEN** the projectile and enemy are flagged as colliding and damage is applied

#### Scenario: Damage applied to enemy on hit
- **WHEN** a projectile collides with an enemy
- **THEN** the enemy's health is reduced by the projectile's damage value

#### Scenario: Area-of-effect damage (cannon shots)
- **WHEN** a cannon projectile hits an area
- **THEN** all enemies within the AoE radius take damage (reduced with distance or flat)

### Requirement: Projectile visual representation
The system SHALL display projectiles with distinct visual models and properties based on tower type.

#### Scenario: Gun tower projectile rendered as sphere
- **WHEN** a gun tower fires
- **THEN** a small sphere projectile appears and travels to the target

#### Scenario: Cannon tower projectile rendered differently
- **WHEN** a cannon tower fires
- **THEN** a larger projectile appears with a distinct color/material indicating cannon shot

#### Scenario: Projectile color indicates tower type
- **WHEN** projectiles from different tower types are in flight
- **THEN** each type has a visually distinct color (e.g., gun = yellow, cannon = red)

### Requirement: Projectile trajectory and speed
The system SHALL support configurable projectile speed and trajectory for different tower types.

#### Scenario: Projectile speed is tunable per tower
- **WHEN** a tower type defines projectile speed
- **THEN** projectiles from that tower travel at the configured speed toward target

#### Scenario: Projectile lead targeting (future position)
- **WHEN** a tower fires at a moving enemy
- **THEN** projectile is aimed toward the enemy's predicted future position, not current position

### Requirement: Projectile effects and feedback
The system SHALL provide visual feedback when projectiles hit their targets.

#### Scenario: Impact particle effect
- **WHEN** a projectile hits an enemy
- **THEN** a brief particle effect (explosion, spark) appears at impact location

#### Scenario: Hit sound effect
- **WHEN** a projectile hits an enemy
- **THEN** an audio effect plays to provide audio feedback (MVP: optional, may be post-implementation)
