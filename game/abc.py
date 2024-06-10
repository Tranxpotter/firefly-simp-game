from abc import ABC, abstractmethod
from typing import TypeVar, Any, Sequence, Optional, Type

class Behavior(ABC):
    def __init__(self, *, active:bool = True) -> None:
        self.active = active
    
    def handle_event(self, event) -> None:...
    
    def update(self, dt:float) -> None:...
    
    def draw(self, screen) -> None:...

    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False
    
    @classmethod
    def register_event(cls) -> Optional[Any]:...

class GameObject(ABC):
    instances:dict[Any, list] = {}
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        if cls.instances.get(cls, None) is not None:
            cls.instances[cls].append(instance)
        else:
            cls.instances[cls] = [instance]
        
        return instance
    
    def __init__(self, game_manager, position:tuple[float, float], size:tuple[float, float], velocity:tuple[float, float] = (0, 0), behaviors:Sequence[Behavior] = []) -> None:
        self.game_manager = game_manager
        game_manager.add_object(self)
        self.position = self.x, self.y = position
        self.size = self.width, self.height = size
        self.velocity = self.velocity_x, self.velocity_y = velocity
        self.behaviors = behaviors
        self.alive = True
    
    @property
    def rect(self):
        return (self.x, self.y, self.width, self.height)
    
    @property
    def area(self):
        return self.width * self.height
    
    def has_behavior(self, behavior:Type[Behavior]):
        '''Checks if the object has a certain type of behavior active'''
        for obj_behavior in self.behaviors:
            if isinstance(obj_behavior, behavior) and obj_behavior.active:
                return True
        return False
    
    
    def on_destroy(self):
        self.alive = False
        self.game_manager.req_delete_object(self)
    
    