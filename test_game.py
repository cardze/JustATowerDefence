#!/usr/bin/env python3
"""
Test script for Tower Defence game
Tests core game mechanics without requiring display
"""
import sys
import os

# Set SDL to use dummy video driver for headless testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame
from tower_defence.app.game import Game
from tower_defence.entities.enemy import Enemy
from tower_defence.entities.projectile import Projectile
from tower_defence.towers.tower import Tower
from tower_defence.core.config import *


def test_enemy_creation():
    """Test enemy creation and initialization"""
    path = [(0, 0), (100, 0), (100, 100)]
    enemy = Enemy(path, wave_number=1)
    
    assert enemy.x == 0
    assert enemy.y == 0
    assert enemy.health > 0
    assert enemy.path_index == 0
    assert not enemy.reached_end
    print("✓ Enemy creation test passed")


def test_enemy_movement():
    """Test enemy movement along path"""
    path = [(0, 0), (100, 0)]
    enemy = Enemy(path, wave_number=1)
    
    initial_x = enemy.x
    enemy.move()
    
    assert enemy.x > initial_x, "Enemy should move forward"
    print("✓ Enemy movement test passed")


def test_enemy_damage():
    """Test enemy taking damage"""
    path = [(0, 0), (100, 0)]
    enemy = Enemy(path, wave_number=1)
    
    initial_health = enemy.health
    is_dead = enemy.take_damage(50)
    
    assert enemy.health < initial_health, "Enemy health should decrease"
    assert not is_dead, "Enemy should not be dead yet"
    
    enemy.take_damage(1000)
    assert enemy.health <= 0, "Enemy should be dead"
    print("✓ Enemy damage test passed")


def test_tower_creation():
    """Test tower creation"""
    tower = Tower(100, 100)
    
    assert tower.x == 100
    assert tower.y == 100
    assert tower.damage > 0
    assert tower.range > 0
    print("✓ Tower creation test passed")


def test_tower_targeting():
    """Test tower finding targets"""
    tower = Tower(100, 100)
    path = [(50, 50), (200, 200)]
    
    # Create enemy in range
    enemy_in_range = Enemy(path, wave_number=1)
    enemy_in_range.x = 120
    enemy_in_range.y = 120
    
    # Create enemy out of range
    enemy_out_range = Enemy(path, wave_number=1)
    enemy_out_range.x = 500
    enemy_out_range.y = 500
    
    enemies = [enemy_in_range, enemy_out_range]
    target = tower.find_target(enemies)
    
    assert target == enemy_in_range, "Tower should target enemy in range"
    print("✓ Tower targeting test passed")


def test_projectile_creation():
    """Test projectile creation"""
    path = [(0, 0), (100, 0)]
    target = Enemy(path, wave_number=1)
    projectile = Projectile(0, 0, target, 10)
    
    assert projectile.target == target
    assert projectile.damage == 10
    print("✓ Projectile creation test passed")


def test_game_initialization():
    """Test game state initialization"""
    pygame.init()
    game = Game()
    
    assert game.money > 0, "Game should start with money"
    assert game.lives > 0, "Game should start with lives"
    assert game.wave_number == 0, "Game should start at wave 0"
    assert len(game.enemies) == 0, "Game should start with no enemies"
    assert len(game.towers) == 0, "Game should start with no towers"
    print("✓ Game initialization test passed")


def test_wave_start():
    """Test starting a wave"""
    pygame.init()
    game = Game()
    
    initial_wave = game.wave_number
    game.start_wave()
    
    assert game.wave_number == initial_wave + 1, "Wave number should increment"
    assert game.wave_in_progress, "Wave should be in progress"
    assert game.enemies_to_spawn > 0, "Should have enemies to spawn"
    print("✓ Wave start test passed")


def test_tower_placement():
    """Test placing towers"""
    pygame.init()
    game = Game()
    
    initial_money = game.money
    initial_tower_count = len(game.towers)
    
    # Place tower in valid position
    success = game.add_tower(400, 300)
    
    assert success, "Tower placement should succeed"
    assert len(game.towers) == initial_tower_count + 1, "Should have one more tower"
    assert game.money < initial_money, "Money should decrease"
    print("✓ Tower placement test passed")


def test_game_update():
    """Test game update loop"""
    pygame.init()
    game = Game()
    
    # Start a wave and spawn an enemy
    game.start_wave()
    game.spawn_enemy()
    
    assert len(game.enemies) > 0, "Should have spawned an enemy"
    
    # Update game
    game.update()
    
    # Game should process without errors
    print("✓ Game update test passed")


def test_tower_upgrade():
    """Test tower upgrade functionality"""
    pygame.init()
    game = Game()
    
    # Add a tower
    game.add_tower(400, 300)
    tower = game.towers[0]
    
    initial_level = tower.level
    initial_damage = tower.damage
    initial_range = tower.range
    
    # Upgrade tower
    success = game.upgrade_tower(tower)
    
    assert success, "Tower upgrade should succeed"
    assert tower.level == initial_level + 1, "Tower level should increase"
    assert tower.damage > initial_damage, "Tower damage should increase"
    assert tower.range > initial_range, "Tower range should increase"
    print("✓ Tower upgrade test passed")


def test_tower_max_upgrade():
    """Test tower cannot exceed max level"""
    pygame.init()
    game = Game()
    
    # Add a tower and give enough money
    game.add_tower(400, 300)
    game.money = 1000
    tower = game.towers[0]
    
    # Upgrade to max level
    while tower.can_upgrade():
        game.upgrade_tower(tower)
    
    assert tower.level == TOWER_MAX_LEVEL, "Tower should reach max level"
    assert not tower.can_upgrade(), "Tower should not be upgradeable at max level"
    print("✓ Tower max upgrade test passed")


def test_path_generation():
    """Test dynamic path generation"""
    pygame.init()
    game = Game()
    
    initial_path = game.path.copy()
    
    # Generate new path
    game.generate_complex_path()
    
    assert game.path != initial_path, "Path should change after generation"
    assert len(game.path) > 0, "Path should not be empty"
    print("✓ Path generation test passed")


def test_restart_level_resets_wave():
    """Test restart level resets wave to 1"""
    pygame.init()
    game = Game()
    
    # Advance to wave 3
    game.wave_number = 3
    game.start_wave()
    
    # Restart level
    game.restart_level()
    
    assert game.wave_number == 0, "Wave number should reset to 0"
    print("✓ Restart level - wave reset test passed")


def test_restart_level_clears_towers():
    """Test restart level removes all towers"""
    pygame.init()
    game = Game()
    game.money = 1000
    
    # Add multiple towers
    game.add_tower(400, 300)
    game.add_tower(600, 400)
    
    assert len(game.towers) > 0, "Should have towers before restart"
    
    # Restart level
    game.restart_level()
    
    assert len(game.towers) == 0, "All towers should be removed"
    print("✓ Restart level - towers cleared test passed")


def test_restart_level_resets_money():
    """Test restart level resets money to initial amount"""
    pygame.init()
    game = Game()
    
    initial_money = game.money
    game.money = 100
    
    # Restart level
    game.restart_level()
    
    assert game.money == initial_money, "Money should reset to initial amount"
    print("✓ Restart level - money reset test passed")


def test_restart_level_resets_lives():
    """Test restart level resets lives to initial amount"""
    pygame.init()
    game = Game()
    
    initial_lives = game.lives
    game.lives = 1
    
    # Restart level
    game.restart_level()
    
    assert game.lives == initial_lives, "Lives should reset to initial amount"
    print("✓ Restart level - lives reset test passed")


def test_restart_level_clears_enemies():
    """Test restart level removes all enemies"""
    pygame.init()
    game = Game()
    
    # Start a wave and spawn enemies
    game.start_wave()
    game.spawn_enemy()
    game.spawn_enemy()
    
    assert len(game.enemies) > 0, "Should have enemies before restart"
    
    # Restart level
    game.restart_level()
    
    assert len(game.enemies) == 0, "All enemies should be removed"
    print("✓ Restart level - enemies cleared test passed")


def test_restart_level_resets_speed_multiplier():
    """Test restart level resets speed multiplier"""
    pygame.init()
    game = Game()
    
    initial_speed = game.speed_multiplier
    game.speed_multiplier = 2.0
    
    # Restart level
    game.restart_level()
    
    assert game.speed_multiplier == initial_speed, "Speed multiplier should reset"
    print("✓ Restart level - speed multiplier reset test passed")


def test_restart_level_stops_wave():
    """Test restart level stops current wave"""
    pygame.init()
    game = Game()
    
    # Start a wave
    game.start_wave()
    assert game.wave_in_progress, "Wave should be in progress"
    
    # Restart level
    game.restart_level()
    
    assert not game.wave_in_progress, "Wave should be stopped"
    print("✓ Restart level - wave stopped test passed")


def test_dog_tower_creation():
    """Test dog tower can be created"""
    pygame.init()
    game = Game()
    game.money = 1000
    game.selected_tower_type = 'dog'
    
    success = game.add_tower(400, 300)
    
    assert success, "Dog tower should be placed successfully"
    assert len(game.towers) == 1, "Should have one tower"
    tower = game.towers[0]
    assert tower.tower_type == 'dog', "Tower should be dog type"
    print("✓ Dog tower creation test passed")


def test_dog_tower_petting_generates_money():
    """Test petting dog tower generates $1"""
    pygame.init()
    game = Game()
    game.money = 1000
    game.selected_tower_type = 'dog'
    
    # Add dog tower
    game.add_tower(400, 300)
    dog_tower = game.towers[0]
    
    initial_money = game.money
    game.pet_money_tower(dog_tower)
    
    assert game.money == initial_money + 1, "Should gain $1 from petting"
    print("✓ Dog tower petting generates money test passed")


def test_dog_tower_multiple_pets():
    """Test multiple pets generate multiple dollars"""
    pygame.init()
    game = Game()
    game.money = 1000
    game.selected_tower_type = 'dog'
    
    # Add dog tower
    game.add_tower(400, 300)
    dog_tower = game.towers[0]
    
    initial_money = game.money
    for _ in range(5):
        game.pet_money_tower(dog_tower)
    
    assert game.money == initial_money + 5, "Should gain $5 from 5 pets"
    print("✓ Dog tower multiple pets test passed")


def test_enemy_reward_reduced_by_25():
    """Test enemy rewards are reduced by 25%"""
    pygame.init()
    game = Game()
    
    path = [(0, 0), (100, 0)]
    enemy = Enemy(path, wave_number=1, enemy_type='basic')
    
    # Original basic enemy reward is 10, after 25% reduction should be 7.5 (rounded to 7)
    expected_reward = int(ENEMY_TYPES['basic']['reward'] * ENEMY_REWARD_REDUCTION_FACTOR)
    
    assert enemy.reward == expected_reward, f"Enemy reward should be {expected_reward}, got {enemy.reward}"
    print("✓ Enemy reward reduced test passed")


def test_dog_tower_has_correct_stats():
    """Test dog tower has correct cost and stats"""
    dog_config = TOWER_TYPES['dog']
    
    assert dog_config['cost'] == 75, "Dog tower should cost $75"
    assert dog_config['name'] == 'Dog Tower', "Should have correct name"
    print("✓ Dog tower stats test passed")


def run_all_tests():
    """Run all tests"""
    print("Running Tower Defence Game Tests...")
    print("-" * 50)
    
    tests = [
        test_enemy_creation,
        test_enemy_movement,
        test_enemy_damage,
        test_tower_creation,
        test_tower_targeting,
        test_projectile_creation,
        test_game_initialization,
        test_wave_start,
        test_tower_placement,
        test_game_update,
        test_tower_upgrade,
        test_tower_max_upgrade,
        test_path_generation,
        test_restart_level_resets_wave,
        test_restart_level_clears_towers,
        test_restart_level_resets_money,
        test_restart_level_resets_lives,
        test_restart_level_clears_enemies,
        test_restart_level_resets_speed_multiplier,
        test_restart_level_stops_wave,
        test_dog_tower_creation,
        test_dog_tower_petting_generates_money,
        test_dog_tower_multiple_pets,
        test_enemy_reward_reduced_by_25,
        test_dog_tower_has_correct_stats
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("-" * 50)
    print(f"Tests completed: {len(tests) - failed}/{len(tests)} passed")
    
    if failed == 0:
        print("All tests passed! ✓")
        return 0
    else:
        print(f"{failed} tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
