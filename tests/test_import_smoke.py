"""Smoke tests for the reorganized package layout."""

from tower_defence.app.game import Game
from tower_defence.combat.attack_strategy import ClosestEnemyStrategy
from tower_defence.core.config import TOWER_TYPES
from tower_defence.entities.enemy import Enemy
from tower_defence.entities.projectile import Projectile
from tower_defence.systems.event_system import EventManager, GameEvent
from tower_defence.towers.tower import Tower
from tower_defence.towers.tower_builder import TowerBuilder
from tower_defence.towers.tower_state import IdleState


def test_package_imports_resolve():
    """Package imports should resolve from their responsibility-based modules."""
    path = [(0, 0), (100, 0)]

    tower = Tower(50, 50)
    enemy = Enemy(path)
    projectile = Projectile(50, 50, enemy, tower.damage)
    builder = TowerBuilder("basic")
    event_manager = EventManager()
    strategy = ClosestEnemyStrategy()
    state = IdleState()
    game = Game()

    assert tower.tower_type in TOWER_TYPES
    assert enemy.enemy_type == "basic"
    assert projectile.damage == tower.damage
    assert builder.tower_type == "basic"
    assert event_manager is not None
    assert strategy is not None
    assert state.get_state_name() == "Idle"
    assert game.wave_number == 0
    assert GameEvent.MONEY_CHANGED.value == "money_changed"
