"""
Observer Pattern: Event system for tower defence game

This module implements an event system where different components can observe
and react to game events like enemies entering range, towers upgrading, etc.
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Callable, Dict


class GameEvent(Enum):
    """Types of events in the game"""
    ENEMY_SPAWNED = "enemy_spawned"
    ENEMY_KILLED = "enemy_killed"
    ENEMY_ESCAPED = "enemy_escaped"
    TOWER_PLACED = "tower_placed"
    TOWER_UPGRADED = "tower_upgraded"
    TOWER_SOLD = "tower_sold"
    ENEMY_IN_RANGE = "enemy_in_range"
    ENEMY_OUT_OF_RANGE = "enemy_out_of_range"
    WAVE_STARTED = "wave_started"
    WAVE_COMPLETED = "wave_completed"
    GAME_OVER = "game_over"
    MONEY_CHANGED = "money_changed"
    LIVES_CHANGED = "lives_changed"


class Observer(ABC):
    """Abstract base class for observers"""
    
    @abstractmethod
    def update(self, event: GameEvent, data: dict = None):
        """
        Called when an observed event occurs
        
        Args:
            event: The event that occurred
            data: Additional data about the event
        """
        pass


class EventManager:
    """
    Central event management system
    
    Manages subscriptions to events and dispatches events to all interested observers.
    Uses singleton pattern to ensure there's only one event manager.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize event manager"""
        if self._initialized:
            return
        
        self.observers: Dict[GameEvent, List[Observer]] = {}
        self.callbacks: Dict[GameEvent, List[Callable]] = {}
        self._initialized = True
    
    def subscribe(self, event: GameEvent, observer: Observer):
        """
        Subscribe an observer to an event
        
        Args:
            event: The event to observe
            observer: The observer object
        """
        if event not in self.observers:
            self.observers[event] = []
        
        if observer not in self.observers[event]:
            self.observers[event].append(observer)
    
    def unsubscribe(self, event: GameEvent, observer: Observer):
        """
        Unsubscribe an observer from an event
        
        Args:
            event: The event to stop observing
            observer: The observer object
        """
        if event in self.observers and observer in self.observers[event]:
            self.observers[event].remove(observer)
    
    def subscribe_callback(self, event: GameEvent, callback: Callable):
        """
        Subscribe a callback function to an event
        
        Args:
            event: The event to observe
            callback: The callback function to call
        """
        if event not in self.callbacks:
            self.callbacks[event] = []
        
        if callback not in self.callbacks[event]:
            self.callbacks[event].append(callback)
    
    def unsubscribe_callback(self, event: GameEvent, callback: Callable):
        """
        Unsubscribe a callback function from an event
        
        Args:
            event: The event to stop observing
            callback: The callback function
        """
        if event in self.callbacks and callback in self.callbacks[event]:
            self.callbacks[event].remove(callback)
    
    def emit(self, event: GameEvent, data: dict = None):
        """
        Emit an event to all subscribed observers
        
        Args:
            event: The event to emit
            data: Additional data to pass with the event
        """
        # Notify all observer objects
        if event in self.observers:
            for observer in self.observers[event]:
                observer.update(event, data)
        
        # Call all callback functions
        if event in self.callbacks:
            for callback in self.callbacks[event]:
                callback(event, data)
    
    def clear(self):
        """Clear all subscriptions (useful for testing)"""
        self.observers.clear()
        self.callbacks.clear()


class GameEventObserver(Observer):
    """Example observer that logs game events"""
    
    def __init__(self, name: str = "GameEventObserver"):
        self.name = name
    
    def update(self, event: GameEvent, data: dict = None):
        """Handle event"""
        print(f"[{self.name}] Event: {event.value}, Data: {data}")


class TowerEventObserver(Observer):
    """Observer that handles tower-related events"""
    
    def __init__(self, tower):
        self.tower = tower
    
    def update(self, event: GameEvent, data: dict = None):
        """Handle tower events"""
        if event == GameEvent.ENEMY_IN_RANGE:
            # Tower can react to enemy entering range
            pass
        elif event == GameEvent.ENEMY_OUT_OF_RANGE:
            # Tower can react to enemy leaving range
            pass
        elif event == GameEvent.TOWER_UPGRADED:
            # Handle upgrade event
            pass


class EnemyEventObserver(Observer):
    """Observer that handles enemy-related events"""
    
    def __init__(self, enemy):
        self.enemy = enemy
    
    def update(self, event: GameEvent, data: dict = None):
        """Handle enemy events"""
        if event == GameEvent.ENEMY_KILLED:
            # Handle enemy death
            pass
        elif event == GameEvent.ENEMY_ESCAPED:
            # Handle escape
            pass


class UIEventObserver(Observer):
    """Observer that updates UI when events occur"""
    
    def __init__(self, ui):
        self.ui = ui
        self.event_log = []
    
    def update(self, event: GameEvent, data: dict = None):
        """Update UI based on event"""
        self.event_log.append((event, data))
        
        if event == GameEvent.MONEY_CHANGED:
            # Update money display
            pass
        elif event == GameEvent.LIVES_CHANGED:
            # Update lives display
            pass
        elif event == GameEvent.WAVE_COMPLETED:
            # Show wave completion message
            pass
        elif event == GameEvent.GAME_OVER:
            # Show game over screen
            pass
    
    def get_recent_events(self, count: int = 5) -> list:
        """Get recent events for display"""
        return self.event_log[-count:]
