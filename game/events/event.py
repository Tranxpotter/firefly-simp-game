# Collision between circle and rectangle to be added!

from abc import ABC, abstractmethod
from typing import TypeVar, Type, Callable, Tuple, Literal, Iterable
from dataclasses import dataclass

from .event_args import _EventArgType, ObjectsArg
from ..game_object import GameObject

GameObj = TypeVar("GameObj", bound=GameObject)
E_Arg = TypeVar("E_Arg", bound=_EventArgType)



class Event(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):...
    
    @abstractmethod
    def get_run_args(self) -> list[_EventArgType]:...
    
    def _get_run_args_str(self) -> str:
        return "(" + ", ".join([str(arg) for arg in self.get_run_args()]) + ")"
        
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
    
    def run(self, *args, **kwargs):
        objs1, objs2, *_ = args
        if not isinstance(objs1, Iterable) or not isinstance(objs2, Iterable) or _:
            raise TypeError(f"Argument type mismatch. Expected: {self._get_run_args_str()}, Got: ({Type(objs1)}, {Type(objs2)})")
        for obj1 in objs1:
            for obj2 in objs2:
                if not isinstance(obj1, self.cls1) or not isinstance(obj2, self.cls2):
                    raise TypeError(f"Types of objects given not match types expected. {type(obj1)}->{self.cls1}, {type(obj2)}->{self.cls2}")
                if not self.is_colliding(obj1, obj2):
                    continue
                self.action(obj1, obj2)
    
    def get_run_args(self) -> list[_EventArgType]:
        return [ObjectsArg(self.cls1), ObjectsArg(self.cls2)]

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
    
    def run(self, *args, **kwargs):
        objs1, objs2, *_ = args
        if not isinstance(objs1, Iterable) or not isinstance(objs2, Iterable) or _:
            raise TypeError(f"Argument type mismatch. Expected: {self._get_run_args_str()}, Got: ({Type(objs1)}, {Type(objs2)})")
        for obj1 in objs1:
            for obj2 in objs2:
                if not isinstance(obj1, self.cls1) or not isinstance(obj2, self.cls2):
                    raise TypeError(f"Types of objects given not match types expected. {type(obj1)}->{self.cls1}, {type(obj2)}->{self.cls2}")
                overlapping, area = self.is_overlapping(obj1, obj2)
                if not overlapping:
                    continue
                
                overlap_info = OverlapInfo(area, obj1.area/area, obj2.area/area)
                self.action(obj1, obj2, overlap_info)
    
    def get_run_args(self) -> list[_EventArgType]:
        return [ObjectsArg(self.cls1), ObjectsArg(self.cls2)]