## 1. Define Target Structure

- [x] 1.1 Map current modules to responsibility-based package groups (game flow, entities, towers, combat/mechanics, support).
- [x] 1.2 Create target directory/package skeletons and `__init__.py` files needed for clear import boundaries.
- [x] 1.3 Document module placement and naming conventions in developer docs before moving code.

## 2. Migrate Modules Safely

- [x] 2.1 Move low-dependency modules into target packages and update direct imports.
- [x] 2.2 Introduce temporary compatibility import shims for moved modules where immediate full migration is not feasible.
- [x] 2.3 Move core orchestration modules and update cross-package references to final paths.

## 3. Preserve Behavior and Validate

- [x] 3.1 Add or update import smoke checks to detect module resolution regressions after each move phase.
- [x] 3.2 Run and fix test suite issues caused by structural migration without changing gameplay behavior.
- [x] 3.3 Remove temporary shims once all references are migrated and checks pass.

## 4. Finalize Documentation and Cleanup

- [x] 4.1 Update README and architecture/codebase docs to reflect the final project layout.
- [x] 4.2 Verify there are no stale path references in scripts, docs, or test configuration.
- [x] 4.3 Perform a final parity pass confirming startup and core loop behavior remain unchanged.
