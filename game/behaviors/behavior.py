import math
from typing import Generic, Type

from ..events import Event, ObjectsArg, EventArgument
from ..abc import Behavior, GameObject
from .._typevars import GameObj

class Anchor(Behavior):
    ...

class Immovable(Behavior):
    ...

class Projectile(Behavior, Generic[GameObj]):
    def __init__(self, speed:float, angle:float, ref:GameObj, accel:float = 0, *, active:bool = True) -> None:
        self.speed = speed
        self.angle = angle
        self._ref = ref
        self.accel = accel
        self.active = active
    
    def update(self, dt: float) -> None:
        if not self.active:
            return
        speed_change = self.speed*self.accel*dt/2
        self.speed += speed_change
        magnitude = self.speed*dt
        move_x, move_y = magnitude*math.cos(self.angle), magnitude*math.sin(self.angle)
        self._ref.x += move_x
        self._ref.y += move_y
        self.speed += speed_change
    
    

class Gravity(Behavior, Generic[GameObj]):
    def __init__(self, ref:GameObj, accel:float = 9.81, terminal_velo:float|None = None, *, active:bool = True) -> None:
        self.accel = accel
        self.terminal_velo = terminal_velo
        self._ref = ref
        self.active = active
    
    def update(self, dt: float) -> None:
        if not self.active:
            return
        curr_velo = self._ref.velocity_y
        velo_change = -self.accel * dt
        self._ref.velocity_y += velo_change if self.terminal_velo and curr_velo + velo_change > self.terminal_velo else 0


class _SolidEvent(Event):
    def __init__(self, solids:set[Type[GameObject]]) -> None:
        self.solids = solids
    
    
    @staticmethod
    def is_overlapping(rect1, rect2):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2

        # Check if the rectangles are not overlapping
        if (x1 + w1 < x2 or x2 + w2 < x1 or
            y1 + h1 < y2 or y2 + h2 < y1):
            return False

        # If they overlap, return True
        return True
    
    @staticmethod
    def resolve_overlap(obj1:GameObject, obj2:GameObject):
        if not obj1.alive or not obj2.alive:
            return
        obj1_movable = not obj1.has_behavior(Immovable)
        obj2_movable = not obj2.has_behavior(Immovable)
        if not obj1_movable and not obj2_movable:
            return
        
        x1, y1, w1, h1 = obj1.rect
        x2, y2, w2, h2 = obj2.rect
        
        overlap_x = min(x1 + w1, x2 + w2) - max(x1, x2)
        overlap_y = min(y1 + h1, y2 + h2) - max(y1, y2)
        
        if overlap_x <= overlap_y:
            if not obj2_movable:
                if x1 < x2:
                    obj1.x -= overlap_x
                else:
                    obj1.x += overlap_x
            elif not obj1_movable:
                if x2 < x1:
                    obj2.x -= overlap_x
                else:
                    obj2.x += overlap_x
            else:
                overlap_x /= 2
                if x1 < x2:
                    obj1.x -= overlap_x
                    obj2.x += overlap_x
                else:
                    obj1.x += overlap_x
                    obj2.x -= overlap_x
        
        else:
            if not obj2_movable:
                if y1 < y2:
                    obj1.y -= overlap_y
                else:
                    obj1.y += overlap_y
            elif not obj1_movable:
                if y2 < y1:
                    obj2.y -= overlap_y
                else:
                    obj2.y += overlap_y
            else:
                overlap_y /= 2
                if y1 < y2:
                    obj1.y -= overlap_y
                    obj2.y += overlap_y
                else:
                    obj1.y += overlap_y
                    obj2.y -= overlap_y
                
        
            
    
    def run(self, *args):
        all_objects:list[GameObject] = []
        for objs in args:
            all_objects += objs
        
        for index1 in range(len(all_objects)):
            for index2 in range(index1+1, len(all_objects)):
                obj1, obj2 = all_objects[index1], all_objects[index2]
                if not obj1.alive or not obj2.alive:
                    continue
                obj1_movable = not obj1.has_behavior(Immovable)
                obj2_movable = not obj2.has_behavior(Immovable)
                if not obj1_movable and not obj2_movable:
                    continue
                overlap = self.is_overlapping(obj1.rect, obj2.rect)
                if not overlap:
                    continue
                self.resolve_overlap(all_objects[index1], all_objects[index2])
    
        
        
        
    
    def get_event_arguments(self) -> list[EventArgument]:
        return [ObjectsArg(solid) for solid in self.solids]


class Solid(Behavior):
    solids:set[Type[GameObject]] = set()
    def __init__(self, ref:GameObject, *, active:bool = True) -> None:
        self._ref = ref
        self.__class__.solids.add(type(ref))
        self.active = active
    
    @classmethod
    def register_event(cls):
        return _SolidEvent(cls.solids)
        
class JumpThru(Behavior):
    ...



class Focus(Behavior):
    ...









