"""
Builder Pattern: Constructing complex tower configurations

This module provides a flexible way to build towers with various configurations,
particularly useful for upgrade systems and different tower types.
"""
from ..core.config import TOWER_TYPES, TOWER_UPGRADE_DAMAGE_BONUS, TOWER_UPGRADE_RANGE_BONUS, TOWER_UPGRADE_FIRE_RATE_BONUS


class TowerBuilder:
    """
    Builder class for creating tower instances with fluent API
    
    Provides a flexible way to configure towers step by step.
    """
    
    def __init__(self, tower_type: str = 'basic'):
        """
        Initialize tower builder
        
        Args:
            tower_type: Type of tower to build
        """
        self.tower_type = tower_type
        self.x = 0
        self.y = 0
        self.level = 1
        self.custom_damage = None
        self.custom_range = None
        self.custom_fire_rate = None
        self.custom_aoe_radius = None
    
    def at_position(self, x: int, y: int):
        """
        Set tower position
        
        Args:
            x, y: Position coordinates
            
        Returns:
            self for chaining
        """
        self.x = x
        self.y = y
        return self
    
    def with_level(self, level: int):
        """
        Set tower level
        
        Args:
            level: Tower level
            
        Returns:
            self for chaining
        """
        self.level = max(1, min(level, 10))  # Clamp between 1-10
        return self
    
    def with_damage(self, damage: int):
        """
        Set custom damage value
        
        Args:
            damage: Damage amount
            
        Returns:
            self for chaining
        """
        self.custom_damage = damage
        return self
    
    def with_range(self, range_val: int):
        """
        Set custom range value
        
        Args:
            range_val: Range distance
            
        Returns:
            self for chaining
        """
        self.custom_range = range_val
        return self
    
    def with_fire_rate(self, fire_rate: int):
        """
        Set custom fire rate
        
        Args:
            fire_rate: Fire rate in frames
            
        Returns:
            self for chaining
        """
        self.custom_fire_rate = fire_rate
        return self
    
    def with_aoe(self, aoe_radius: int):
        """
        Set custom AoE radius
        
        Args:
            aoe_radius: Area of effect radius
            
        Returns:
            self for chaining
        """
        self.custom_aoe_radius = aoe_radius
        return self
    
    def build(self):
        """
        Build and return the tower
        
        Returns:
            Tower instance with configured parameters
        """
        # Import here to avoid circular import
        from .tower import Tower
        
        tower = Tower(self.x, self.y, self.tower_type)
        
        # Apply level-based upgrades
        for _ in range(self.level - 1):
            tower.upgrade()
        
        # Apply custom configurations if provided
        if self.custom_damage is not None:
            tower.damage = self.custom_damage
        
        if self.custom_range is not None:
            tower.range = self.custom_range
        
        if self.custom_fire_rate is not None:
            tower.fire_rate = self.custom_fire_rate
        
        if self.custom_aoe_radius is not None:
            tower.aoe_radius = self.custom_aoe_radius
        
        return tower
    
    def reset(self):
        """Reset builder to default state"""
        self.level = 1
        self.custom_damage = None
        self.custom_range = None
        self.custom_fire_rate = None
        self.custom_aoe_radius = None
        return self


class TowerConfiguration:
    """
    Predefined tower configurations for common setups
    """
    
    @staticmethod
    def basic_tower(x: int, y: int):
        """Create a basic tower configuration"""
        return (TowerBuilder('basic')
                .at_position(x, y)
                .with_level(1)
                .build())
    
    @staticmethod
    def upgraded_tower(x: int, y: int, level: int = 3):
        """Create an upgraded tower"""
        return (TowerBuilder('basic')
                .at_position(x, y)
                .with_level(level)
                .build())
    
    @staticmethod
    def sniper_tower(x: int, y: int):
        """Create a sniper tower for long-range attacks"""
        return (TowerBuilder('sniper')
                .at_position(x, y)
                .with_level(1)
                .build())
    
    @staticmethod
    def rapid_fire_tower(x: int, y: int):
        """Create a rapid fire tower"""
        return (TowerBuilder('rapid')
                .at_position(x, y)
                .with_level(1)
                .build())
    
    @staticmethod
    def cannon_tower(x: int, y: int):
        """Create a cannon tower with AoE damage"""
        return (TowerBuilder('cannon')
                .at_position(x, y)
                .with_level(1)
                .build())
    
    @staticmethod
    def custom_tower(tower_type: str, x: int, y: int, **kwargs):
        """
        Create a custom configured tower
        
        Args:
            tower_type: Type of tower
            x, y: Position
            **kwargs: Additional configuration (level, damage, range, etc.)
            
        Returns:
            Configured tower
        """
        builder = TowerBuilder(tower_type).at_position(x, y)
        
        if 'level' in kwargs:
            builder.with_level(kwargs['level'])
        
        if 'damage' in kwargs:
            builder.with_damage(kwargs['damage'])
        
        if 'range' in kwargs:
            builder.with_range(kwargs['range'])
        
        if 'fire_rate' in kwargs:
            builder.with_fire_rate(kwargs['fire_rate'])
        
        if 'aoe' in kwargs:
            builder.with_aoe(kwargs['aoe'])
        
        return builder.build()


class TowerUpgradeBuilder:
    """
    Builder specifically for handling tower upgrades
    """
    
    def __init__(self, tower):
        """
        Initialize upgrade builder with existing tower
        
        Args:
            tower: The tower to upgrade
        """
        self.tower = tower
        self.levels = 1
        self.bonus_damage = 0
        self.bonus_range = 0
        self.fire_rate_reduction = 0
    
    def upgrade_levels(self, num_levels: int):
        """
        Upgrade tower by multiple levels
        
        Args:
            num_levels: Number of levels to upgrade
            
        Returns:
            self for chaining
        """
        self.levels = num_levels
        return self
    
    def add_damage_bonus(self, bonus: int):
        """
        Add damage bonus on top of normal upgrades
        
        Args:
            bonus: Bonus damage
            
        Returns:
            self for chaining
        """
        self.bonus_damage = bonus
        return self
    
    def add_range_bonus(self, bonus: int):
        """
        Add range bonus
        
        Args:
            bonus: Bonus range
            
        Returns:
            self for chaining
        """
        self.bonus_range = bonus
        return self
    
    def reduce_fire_rate(self, reduction: int):
        """
        Reduce fire rate (lower is faster)
        
        Args:
            reduction: Fire rate reduction
            
        Returns:
            self for chaining
        """
        self.fire_rate_reduction = reduction
        return self
    
    def apply(self):
        """
        Apply the upgrade to the tower
        
        Returns:
            bool: True if upgrade was successful
        """
        for _ in range(self.levels):
            if not self.tower.can_upgrade():
                return False
            self.tower.upgrade()
        
        # Apply additional bonuses
        self.tower.damage += self.bonus_damage
        self.tower.range += self.bonus_range
        self.tower.fire_rate = max(5, self.tower.fire_rate - self.fire_rate_reduction)
        
        return True
    
    def reset(self):
        """Reset upgrade builder"""
        self.levels = 1
        self.bonus_damage = 0
        self.bonus_range = 0
        self.fire_rate_reduction = 0
        return self
