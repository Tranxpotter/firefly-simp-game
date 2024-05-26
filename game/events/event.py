# Collision between circle and rectangle to be added!

from abc import ABC, abstractmethod
from typing import TypeVar, Type, Callable, Tuple
from dataclasses import dataclass

from game_object import GameObject

GameObj = TypeVar("GameObj", bound=GameObject)

class Event(ABC):
    @abstractmethod
    def run(self, obj1:GameObj, obj2:GameObj):...
        
from .manager import EventManager

class Collision(Event):
    def __init__(self, cls1:Type[GameObj], cls2:Type[GameObj], action:Callable[[GameObj, GameObj], None]) -> None:
        self.check_classes = self.cls1, self.cls2 = cls1, cls2
        self.action = action
    
    @staticmethod
    def is_colliding(obj1:GameObj, obj2:GameObj):
        left1, top1, width1, height1 = obj1.rect
        right1, bottom1 = left1 + width1, top1 + height1
        
        left2, top2, width2, height2 = obj2.rect
        right2, bottom2 = left2 + width2, top2 + height2
        
        if left1 > right2 or left2 > right1:
            return False
        if top1 > bottom2 or top2 > bottom1:
            return False
        
        return True
    
    def run(self, obj1: GameObj, obj2: GameObj):
        if not isinstance(obj1, self.cls1) or not isinstance(obj2, self.cls2):
            raise TypeError(f"Types of objects given not match types expected. {type(obj1)}->{self.cls1}, {type(obj2)}->{self.cls2}")
        if not self.is_colliding(obj1, obj2):
            return
        
        self.action(obj1, obj2)

@dataclass
class OverlapInfo:
    area:float
    percentage1:float
    percentage2:float
    

class Overlap(Event):
    def __init__(self, cls1:Type[GameObj], cls2:Type[GameObj], action:Callable[[GameObj, GameObj, OverlapInfo], None]) -> None:
        self.check_classes = self.cls1, self.cls2 = cls1, cls2
        self.action = action
    
    @staticmethod
    def is_overlapping(obj1:GameObj, obj2:GameObj) -> tuple[bool, float]:
        left1, top1, width1, height1 = obj1.rect
        right1, bottom1 = left1 + width1, top1 + height1
        
        left2, top2, width2, height2 = obj2.rect
        right2, bottom2 = left2 + width2, top2 + height2
        
        if left1 >= right2 or left2 >= right1:
            return False, 0
        if top1 >= bottom2 or top2 >= bottom1:
            return False, 0
        
        overlap_x = min(abs(left1 - right2), abs(left2 - right1))
        overlap_y = min(abs(top1 - bottom2), abs(top2 - bottom1))
        
        return True, overlap_x * overlap_y
    
    def run(self, obj1: GameObj, obj2: GameObj):
        if not isinstance(obj1, self.cls1) or not isinstance(obj2, self.cls2):
            raise TypeError(f"Types of objects given not match types expected. {type(obj1)}->{self.cls1}, {type(obj2)}->{self.cls2}")
        overlapping, area = self.is_overlapping(obj1, obj2)
        if not overlapping:
            return
        
        overlap_info = OverlapInfo(area, obj1.area/area, obj2.area/area)
        
        self.action(obj1, obj2, overlap_info)
    
