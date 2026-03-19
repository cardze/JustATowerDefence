## ADDED Requirements

### Requirement: 3D tower scene with placement and visual model
The system SHALL support tower entities as individual 3D scenes with mesh representation, position in 3D space, and visual feedback during placement.

#### Scenario: Tower placed in 3D world
- **WHEN** player confirms tower placement at a clicked location
- **THEN** tower appears in the world at (X, Y, Z) with a visible cylindrical mesh

#### Scenario: Tower placement preview shown before confirmation
- **WHEN** player moves mouse over level with tower selected but not yet placed
- **THEN** a semitransparent preview of the tower appears at the raycast position

#### Scenario: Tower placement collision detection
- **WHEN** player attempts to place a tower overlapping an existing tower
- **THEN** system prevents placement and provides visual feedback (e.g., preview turns red)

### Requirement: Tower targeting and range visualization
The system SHALL indicate a tower's attack range as a visual representation and calculate target distance for enemy targeting.

#### Scenario: Tower displays range sphere
- **WHEN** a tower is placed or selected
- **THEN** a spherical outline or wireframe appears around the tower indicating its attack range

#### Scenario: Tower range updates with upgrade
- **WHEN** a tower is upgraded and gains increased range
- **THEN** the range visualization expands to reflect the new range radius

#### Scenario: Range calculation for targeting
- **WHEN** an enemy enters the tower's range sphere
- **THEN** tower performs distance calculation (X, Y, Z coordinates) to determine if enemy is within attacking range

### Requirement: Tower persistence in game world
The system SHALL maintain tower state and position throughout the game scene, with proper scene management and resource cleanup.

#### Scenario: Tower persists after placement
- **WHEN** a tower is placed and the game continues running
- **THEN** the tower remains in the world at its position with consistent behavior

#### Scenario: Multiple towers coexist
- **WHEN** multiple towers are placed in different locations
- **THEN** each tower is a distinct scene node with independent state and targeting

### Requirement: Tower visual feedback for state
The system SHALL provide visual indicators for tower state (idle, targeting, cooling down) through color, material, or animation changes.

#### Scenario: Tower color changes when targeting
- **WHEN** a tower has a valid target in range
- **THEN** the tower's material color changes (e.g., from blue to green) to indicate active state

#### Scenario: Tower cooldown visualization
- **WHEN** a tower has fired and is in cooldown
- **THEN** a visual indicator (color tint or animation) shows the tower is not yet able to fire again
