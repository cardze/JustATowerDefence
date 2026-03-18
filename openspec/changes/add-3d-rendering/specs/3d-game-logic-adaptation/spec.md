## ADDED Requirements

### Requirement: Game state management in Godot (GameManager autoload)
The system SHALL maintain game state (player money, current wave, lives, enemies list, towers list) through an autoload singleton accessible from all scenes.

#### Scenario: GameManager persists across scenes
- **WHEN** a level completes or reloads
- **THEN** GameManager retains state or is reset appropriately for new level

#### Scenario: Money updated on kill
- **WHEN** an enemy dies
- **THEN** GameManager adds the kill reward to player money

#### Scenario: Money deducted on tower purchase
- **WHEN** player places a tower
- **THEN** GameManager subtracts tower cost from player money and prevents placement if insufficient funds

### Requirement: Wave spawning and progression
The system SHALL spawn waves of enemies at configurable intervals with increasing difficulty.

#### Scenario: Wave 1 spawns on game start
- **WHEN** the game level is loaded and started
- **THEN** Wave 1 enemies spawn at the track start with the configured count and type

#### Scenario: Next wave spawns after delay
- **WHEN** all enemies in current wave are defeated
- **THEN** a timer triggers and Wave N+1 spawns after the configured inter-wave delay

#### Scenario: Wave difficulty increases
- **WHEN** waves progress (Wave 2, Wave 3, etc.)
- **THEN** enemy count, health, or speed increases per wave configuration

#### Scenario: Game progresses until wave limit
- **WHEN** player survives a configured maximum wave count
- **THEN** game transitions to win/victory state

### Requirement: Lives and game over condition
The system SHALL track player lives and end the game when lives reach zero.

#### Scenario: Player starts with 20 lives
- **WHEN** the game is initialized
- **THEN** GameManager sets player lives to 20

#### Scenario: Life lost on enemy escape
- **WHEN** an enemy reaches the end of the track
- **THEN** player loses 1 life and enemy is removed

#### Scenario: Game over when lives = 0
- **WHEN** player lives reach 0
- **THEN** game ends and displays game over screen or menu

### Requirement: Tower placement and targeting logic
The system SHALL handle tower placement requests, validate placement, and manage tower targeting against enemies.

#### Scenario: Tower placement validated
- **WHEN** player attempts to place a tower
- **THEN** system checks: cost <= money, placement not overlapping, valid location. Place only if all checks pass.

#### Scenario: Tower targets nearest enemy
- **WHEN** a tower is in range of multiple enemies
- **THEN** tower calculates distances and targets the nearest (default strategy)

#### Scenario: Tower fires when on cooldown expired
- **WHEN** tower cooldown timer expires and target is still in range
- **THEN** tower fires a projectile and cooldown resets

### Requirement: Signals and event-driven architecture
The system SHALL use Godot signals to decouple components (towers firing, enemies dying, money changing) so game events propagate without direct coupling.

#### Scenario: Enemy death signal emitted
- **WHEN** an enemy health reaches 0
- **THEN** enemy emits a signal that GameManager listens to for money/wave updates

#### Scenario: Tower targeting signal
- **WHEN** a tower acquires a target
- **THEN** tower emits a signal for UI to update target indicator (optional)

#### Scenario: Money changed signal
- **WHEN** GameManager money value changes
- **THEN** GameManager emits a signal that UI listens to for display update

### Requirement: Game loop and update cycle
The system SHALL implement a continuous game loop with tower updates, enemy movement, projectile updates, and collision detection.

#### Scenario: Game runs at consistent FPS
- **WHEN** the game is running
- **THEN** the game loop executes at target framerate (60 FPS or configurable)

#### Scenario: Enemies move each frame
- **WHEN** the game loop executes
- **THEN** each enemy's position is updated based on time delta and track position

#### Scenario: Towers update targeting each frame
- **WHEN** the game loop executes
- **THEN** each tower recalculates enemies in range and fires if cooldown allows

### Requirement: Game UI for player feedback
The system SHALL display current game state (money, lives, wave number, tower info) to the player.

#### Scenario: HUD displays money and lives
- **WHEN** the game is running
- **THEN** a HUD element shows current money balance and remaining lives

#### Scenario: Wave counter displayed
- **WHEN** a new wave starts
- **THEN** HUD displays "Wave N/Max" or similar

#### Scenario: Selected tower info shown
- **WHEN** player hovers over or selects a tower
- **THEN** tower stats (cost, range, damage, cooldown) are displayed
