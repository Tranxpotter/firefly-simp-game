# Collision between circle and rectangle to be added!

from abc import ABC, abstractmethod
from typing import TypeVar, Type, Callable, Tuple, Literal, Sequence, TypeAlias, List, Generic
from dataclasses import dataclass

from ..abc import GameObject
from .event_args import EventArgument, ObjectsArg

EventArguments:TypeAlias = List[EventArgument]

def _get_types_str(items:Sequence):
    return "(" + ", ".join([str(type(item)) for item in items]) + ")"

class Event(ABC):
    @abstractmethod
    def run(self, *args):...
    """
    Runs the event with the provided arguments.
    
    Args:
        *args: Variable length argument list to be passed to the event.
    """
    
    @abstractmethod
    def get_event_arguments(self) -> EventArguments:...
    """
    Returns the arguments for the current event.
    
    Returns:
        EventArguments: The arguments for the current event.
    """
    
    def _get_expected_run_args_str(self) -> str:
        return "(" + ", ".join([str(arg.get_expected_return_type()) for arg in self.get_event_arguments()]) + ")"


class CollisionEvent(Event):
    def __init__(self, object_type_1:Type[GameObject], object_type_2:Type[GameObject], action:Callable[[GameObject, GameObject], None]) -> None:
        self.check_classes = self.object_type_1, self.object_type_2 = object_type_1, object_type_2
        self.action = action
    
    @staticmethod
    def is_colliding(obj1:GameObject, obj2:GameObject):
        left1, top1, width1, height1 = obj1.rect
        right1, bottom1 = left1 + width1, top1 + height1
        
        left2, top2, width2, height2 = obj2.rect
        right2, bottom2 = left2 + width2, top2 + height2
        
        if left1 > right2 or left2 > right1:
            return False
        if top1 > bottom2 or top2 > bottom1:
            return False
        
        return True
    
    def run(self, *args):
        objs1, objs2, *_ = args
        if not isinstance(objs1, Sequence) or not isinstance(objs2, Sequence):
            raise TypeError(f"Argument type mismatch. Expected: {self._get_expected_run_args_str()}, Got: {_get_types_str(args)}")
        
        for obj1 in objs1:
            for obj2 in objs2:
                if not isinstance(obj1, self.object_type_1) or not isinstance(obj2, self.object_type_2):
                    raise TypeError(f"Types of objects given not match types expected. {type(obj1)}->{self.object_type_1}, {type(obj2)}->{self.object_type_2}")
                if not self.is_colliding(obj1, obj2):
                    continue
                self.action(obj1, obj2)
    
    def get_event_arguments(self) -> EventArguments:
        return [ObjectsArg(self.object_type_1), ObjectsArg(self.object_type_2)]

@dataclass
class OverlapInfo:
    area:float
    percentage1:float
    percentage2:float
    

class OverlapEvent(Event):
    def __init__(self, object_type_1:Type[GameObject], object_type_2:Type[GameObject], action:Callable[[GameObject, GameObject, OverlapInfo], None]) -> None:
        self.check_classes = self.object_type_1, self.object_type_2 = object_type_1, object_type_2
        self.action = action
    
    @staticmethod
    def is_overlapping(obj1:GameObject, obj2:GameObject) -> tuple[bool, float]:
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
    
    def run(self, *args):
        objs1, objs2, *_ = args
        if not isinstance(objs1, Sequence) or not isinstance(objs2, Sequence):
            raise TypeError(f"Argument type mismatch. Expected: {self._get_expected_run_args_str()}, Got: ({Type(objs1)}, {Type(objs2)})")
        for obj1 in objs1:
            for obj2 in objs2:
                if not isinstance(obj1, self.object_type_1) or not isinstance(obj2, self.object_type_2):
                    raise TypeError(f"Types of objects given not match types expected. {type(obj1)}->{self.object_type_1}, {type(obj2)}->{self.object_type_2}")
                overlapping, area = self.is_overlapping(obj1, obj2)
                if not overlapping:
                    continue
                
                overlap_info = OverlapInfo(area, obj1.area/area, obj2.area/area)
                self.action(obj1, obj2, overlap_info)
    
    def get_event_arguments(self) -> EventArguments:
        return [ObjectsArg(self.object_type_1), ObjectsArg(self.object_type_2)]