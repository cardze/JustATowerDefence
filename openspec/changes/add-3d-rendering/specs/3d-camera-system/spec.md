## ADDED Requirements

### Requirement: Isometric fixed camera with pan/zoom controls
The system SHALL provide a fixed camera positioned at an isometric angle (approximately 45°) that allows the player to pan and zoom the view without rotating the world.

#### Scenario: Camera initialization
- **WHEN** the game scene is loaded
- **THEN** the camera is positioned at an isometric angle overlooking the game world and the view is clear and playable

#### Scenario: Player pans camera with arrow keys
- **WHEN** player holds arrow keys (or WASD)
- **THEN** camera translates laterally (pan) without rotating, allowing view of different parts of the level

#### Scenario: Player zooms with scroll wheel
- **WHEN** player scrolls mouse wheel up/down
- **THEN** camera zooms in/out smoothly (field-of-view or distance adjustment) without changing angle or pan

### Requirement: Mouse-to-world raycast for tower placement targeting
The system SHALL cast a ray from the camera through the mouse cursor position to identify the point in 3D world space where the user has clicked.

#### Scenario: Player clicks on terrain
- **WHEN** player clicks left mouse button on a visible part of the level
- **THEN** system calculates the 3D world position at the click location (typically on the terrain plane)

#### Scenario: Click position used for tower preview
- **WHEN** player moves mouse over the level with a tower selected
- **THEN** a tower preview appears at the raycast intersection point on the terrain

### Requirement: Camera bounds and clipping
The system SHALL prevent the camera from panning beyond level boundaries and smooth clipping when zoomed in extreme amounts.

#### Scenario: Camera stops at level edge
- **WHEN** player attempts to pan to a position beyond the level boundary
- **THEN** camera stops at the boundary edge and does not pan further

#### Scenario: Extreme zoom clipping
- **WHEN** player zooms in very close (near-clip plane active)
- **THEN** objects closer than the near-clip plane are not rendered or partially culled

### Requirement: Camera transition and speed control
The system SHALL support smooth camera movement with configurable pan/zoom speed to ensure responsive but controlled player input.

#### Scenario: Pan speed is tunable
- **WHEN** pan speed is defined in a config file or constant
- **THEN** player pan input responds proportionally to the configured speed value

#### Scenario: Zoom speed is tunable
- **WHEN** zoom speed is defined in a config file or constant
- **THEN** player zoom input responds proportionally to the configured speed value
