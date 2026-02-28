"""
State Pattern: Managing tower states (Idle, Attacking, Cooling, Upgraded)

This module defines different states a tower can be in and how it behaves in each state.
"""
from abc import ABC, abstractmethod
from enum import Enum


class TowerState(ABC):
    """Abstract base class for tower states"""
    
    @abstractmethod
    def enter(self, tower):
        """Called when entering this state"""
        pass
    
    @abstractmethod
    def exit(self, tower):
        """Called when exiting this state"""
        pass
    
    @abstractmethod
    def handle_attack(self, tower, enemies):
        """
        Handle attacking in this state
        
        Returns:
            Projectile or None
        """
        pass
    
    @abstractmethod
    def get_state_name(self):
        """Return the name of this state"""
        pass


class IdleState(TowerState):
    """Tower is idle, searching for targets"""
    
    def enter(self, tower):
        """Enter idle state"""
        tower.frames_since_fire = 0
    
    def exit(self, tower):
        """Exit idle state"""
        pass
    
    def handle_attack(self, tower, enemies):
        """Search for targets and transition to attacking state if found"""
        if tower.target:
            tower.state = AttackingState()
            tower.state.enter(tower)
            return tower.state.handle_attack(tower, enemies)
        return None
    
    def get_state_name(self):
        return "Idle"


class AttackingState(TowerState):
    """Tower is actively attacking a target"""
    
    def enter(self, tower):
        """Enter attacking state"""
        tower.frames_since_fire = 0
    
    def exit(self, tower):
        """Exit attacking state"""
        pass
    
    def handle_attack(self, tower, enemies):
        """Attack the current target"""
        # Check if target is still valid
        if not tower.target or tower.target.health <= 0:
            tower.target = None
            tower.state = IdleState()
            tower.state.enter(tower)
            return None
        
        # Check if target is still in range
        target_x, target_y = tower.target.get_position()
        dx = target_x - tower.x
        dy = target_y - tower.y
        distance = (dx**2 + dy**2)**0.5
        
        if distance > tower.range:
            tower.target = None
            tower.state = IdleState()
            tower.state.enter(tower)
            return None
        
        # Fire if ready
        tower.frames_since_fire += 1
        if tower.frames_since_fire >= tower.fire_rate:
            tower.frames_since_fire = 0
            # Import here to avoid circular import
            from projectile import Projectile
            return Projectile(tower.x, tower.y, tower.target, tower.damage, tower.aoe_radius)
        
        return None
    
    def get_state_name(self):
        return "Attacking"


class UpgradedState(TowerState):
    """Tower has been upgraded - enhanced stats"""
    
    def enter(self, tower):
        """Enter upgraded state"""
        pass
    
    def exit(self, tower):
        """Exit upgraded state"""
        pass
    
    def handle_attack(self, tower, enemies):
        """Attack with upgraded stats"""
        # Similar to attacking state but could have special behavior
        if tower.target and tower.target.health > 0:
            target_x, target_y = tower.target.get_position()
            dx = target_x - tower.x
            dy = target_y - tower.y
            distance = (dx**2 + dy**2)**0.5
            
            if distance <= tower.range:
                tower.frames_since_fire += 1
                if tower.frames_since_fire >= tower.fire_rate:
                    tower.frames_since_fire = 0
                    from projectile import Projectile
                    return Projectile(tower.x, tower.y, tower.target, tower.damage, tower.aoe_radius)
        
        return None
    
    def get_state_name(self):
        return "Upgraded"


class CooldownState(TowerState):
    """Tower is in cooldown after attacking"""
    
    def __init__(self, cooldown_frames=10):
        self.cooldown_frames = cooldown_frames
        self.remaining_frames = 0
    
    def enter(self, tower):
        """Enter cooldown state"""
        self.remaining_frames = self.cooldown_frames
    
    def exit(self, tower):
        """Exit cooldown state"""
        pass
    
    def handle_attack(self, tower, enemies):
        """Decrease cooldown timer"""
        self.remaining_frames -= 1
        
        if self.remaining_frames <= 0:
            tower.state = IdleState()
            tower.state.enter(tower)
        
        return None
    
    def get_state_name(self):
        return "Cooldown"


class StateEnum(Enum):
    """Enumeration of possible tower states"""
    IDLE = "idle"
    ATTACKING = "attacking"
    COOLDOWN = "cooldown"
    UPGRADED = "upgraded"
