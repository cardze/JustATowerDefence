"""
Design Patterns Demo for Tower Defence Game

This module demonstrates how to use the refactored game with design patterns:
1. Strategy Pattern - Changing tower attack strategies
2. State Pattern - Tower state management
3. Observer Pattern - Event-driven architecture
4. Builder Pattern - Tower construction
"""

from tower_defence.towers.tower import Tower
from tower_defence.app.game import Game
from tower_defence.systems.event_system import EventManager, GameEvent, GameEventObserver
from tower_defence.towers.tower_builder import TowerBuilder, TowerConfiguration
from tower_defence.combat.attack_strategy import (
    ClosestEnemyStrategy, FastestEnemyStrategy,
    StrongestEnemyStrategy, FarthestEnemyStrategy
)


def demo_strategy_pattern():
    """
    Demonstrate Strategy Pattern usage
    
    Different towers use different attack strategies to target enemies.
    Strategies can be changed at runtime.
    """
    print("\n=== Strategy Pattern Demo ===")
    print("Creating towers with different strategies...\n")
    
    # Create towers
    basic_tower = Tower(100, 100, 'basic')
    sniper_tower = Tower(300, 100, 'sniper')
    rapid_tower = Tower(500, 100, 'rapid')
    
    print(f"Basic Tower - Current Strategy: {type(basic_tower.attack_strategy).__name__}")
    print(f"Sniper Tower - Current Strategy: {type(sniper_tower.attack_strategy).__name__}")
    print(f"Rapid Tower - Current Strategy: {type(rapid_tower.attack_strategy).__name__}")
    
    # Change strategies at runtime
    print("\nChanging strategies dynamically...\n")
    basic_tower.set_attack_strategy(StrongestEnemyStrategy())
    sniper_tower.set_attack_strategy(FarthestEnemyStrategy())
    rapid_tower.set_attack_strategy(FastestEnemyStrategy())
    
    print(f"Basic Tower - New Strategy: {type(basic_tower.attack_strategy).__name__}")
    print(f"Sniper Tower - New Strategy: {type(sniper_tower.attack_strategy).__name__}")
    print(f"Rapid Tower - New Strategy: {type(rapid_tower.attack_strategy).__name__}")


def demo_state_pattern():
    """
    Demonstrate State Pattern usage
    
    Towers can be in different states (Idle, Attacking, Upgraded)
    Each state has different behavior.
    """
    print("\n=== State Pattern Demo ===")
    print("Tower state transitions...\n")
    
    tower = Tower(200, 200, 'basic')
    
    print(f"Initial State: {tower.state.get_state_name()}")
    
    # Upgrade tower
    print("\nUpgrading tower...")
    tower.upgrade()
    print(f"State after upgrade: {tower.state.get_state_name()}")
    
    # Set to attacking state
    from tower_defence.towers.tower_state import AttackingState
    print("\nChanging to attacking state...")
    tower.set_state(AttackingState())
    print(f"Current State: {tower.state.get_state_name()}")


def demo_observer_pattern():
    """
    Demonstrate Observer Pattern usage
    
    Various objects can observe game events and react to them.
    """
    print("\n=== Observer Pattern Demo ===")
    print("Setting up event observers...\n")
    
    # Create event manager
    event_manager = EventManager()
    
    # Create and register observer
    observer = GameEventObserver("Game Logger")
    event_manager.subscribe(GameEvent.TOWER_PLACED, observer)
    event_manager.subscribe(GameEvent.ENEMY_KILLED, observer)
    event_manager.subscribe(GameEvent.TOWER_UPGRADED, observer)
    
    # Emit events
    print("Emitting events...\n")
    
    event_manager.emit(GameEvent.TOWER_PLACED, {
        'position': (100, 100),
        'type': 'basic'
    })
    
    event_manager.emit(GameEvent.TOWER_UPGRADED, {
        'tower_position': (100, 100),
        'new_level': 2
    })
    
    event_manager.emit(GameEvent.ENEMY_KILLED, {
        'enemy_type': 'basic',
        'reward': 10
    })


def demo_builder_pattern():
    """
    Demonstrate Builder Pattern usage
    
    Towers can be constructed with fluent API and predefined configurations.
    """
    print("\n=== Builder Pattern Demo ===")
    print("Building towers with different configurations...\n")
    
    # Using builder for basic tower
    print("1. Building a basic tower with level 1:")
    tower1 = (TowerBuilder('basic')
             .at_position(100, 100)
             .with_level(1)
             .build())
    print(f"   Tower: {tower1.name} at ({tower1.x}, {tower1.y}), Level: {tower1.level}")
    
    # Using builder for upgraded tower
    print("\n2. Building an upgraded basic tower (level 3):")
    tower2 = (TowerBuilder('basic')
             .at_position(200, 100)
             .with_level(3)
             .build())
    print(f"   Tower: {tower2.name} at ({tower2.x}, {tower2.y}), Level: {tower2.level}")
    print(f"   Stats - Damage: {tower2.damage}, Range: {tower2.range}, Fire Rate: {tower2.fire_rate}")
    
    # Using builder with custom stats
    print("\n3. Building a custom configured tower:")
    tower3 = (TowerBuilder('sniper')
             .at_position(300, 100)
             .with_level(2)
             .with_damage(100)
             .with_range(300)
             .build())
    print(f"   Tower: {tower3.name} at ({tower3.x}, {tower3.y}), Level: {tower3.level}")
    print(f"   Custom Stats - Damage: {tower3.damage}, Range: {tower3.range}")
    
    # Using predefined configurations
    print("\n4. Using predefined configurations:")
    cannon = TowerConfiguration.cannon_tower(400, 100)
    print(f"   Tower: {cannon.name} at ({cannon.x}, {cannon.y})")
    print(f"   AoE Radius: {cannon.aoe_radius}")


def demo_game_integration():
    """
    Demonstrate integration of all patterns in the game
    """
    print("\n=== Game Integration Demo ===")
    print("Showing how patterns work together in the game...\n")
    
    # Create game
    game = Game()
    
    # Setup event observer
    event_observer = GameEventObserver("Game UI")
    event_manager = EventManager()
    event_manager.subscribe(GameEvent.TOWER_PLACED, event_observer)
    event_manager.subscribe(GameEvent.MONEY_CHANGED, event_observer)
    
    print(f"Initial State - Money: ${game.money}, Lives: {game.lives}\n")
    
    # Add tower using builder
    print("Adding a tower using builder pattern...")
    if game.add_tower(150, 150, 'basic'):
        print(f"Tower added! Money remaining: ${game.money}\n")
    
    # Change tower strategy
    if game.towers:
        tower = game.towers[0]
        print(f"Tower strategy before: {type(tower.attack_strategy).__name__}")
        game.change_tower_strategy(tower, 'strongest')
        print(f"Tower strategy after: {type(tower.attack_strategy).__name__}\n")
    
    # Upgrade tower
    print("Upgrading tower...")
    if game.towers and game.upgrade_tower(game.towers[0]):
        print(f"Tower upgraded! Money remaining: ${game.money}\n")
    
    print("Demo complete!")


def run_all_demos():
    """Run all design pattern demonstrations"""
    print("=" * 60)
    print("TOWER DEFENCE - DESIGN PATTERNS DEMONSTRATION")
    print("=" * 60)
    
    demo_strategy_pattern()
    demo_state_pattern()
    demo_observer_pattern()
    demo_builder_pattern()
    demo_game_integration()
    
    print("\n" + "=" * 60)
    print("All demonstrations completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_demos()
