from typing import TypeVar, Any

import pygame

from .behavior import Behavior

B = TypeVar("B", bound=Behavior)
class GameObject:
    instances:dict[Any, list] = {}
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        if cls.instances.get(cls, None) is not None:
            cls.instances[cls].append(instance)
        else:
            cls.instances[cls] = [instance]
        
        return instance
    
    def __init__(self, game_manager, position:tuple[float, float], size:tuple[float, float], velocity:tuple[float, float] = (0, 0), properties:list[B] = []) -> None:
        self.game_manager = game_manager
        game_manager.add_object(self)
        self.position = self.x, self.y = position
        self.size = self.width, self.height = size
        self.velocity = self.velocity_x, self.velocity_y = velocity
        self.properties = properties
    
    @property
    def rect(self):
        return (self.x, self.y, self.width, self.height)
    
    @property
    def area(self):
        return self.width * self.height
    
    def on_destroy(self):
        self.game_manager.delete_object(self)
    
    
    