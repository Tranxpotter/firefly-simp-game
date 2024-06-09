import math
from typing import Generic, Type

from ..abc import Behavior, GameObject
from .._typevars import GameObj

class Anchor(Behavior):
    ...

class Projectile(Behavior, Generic[GameObj]):
    def __init__(self, speed:float, angle:float, ref:GameObj, accel:float = 0) -> None:
        self.speed = speed
        self.angle = angle
        self._ref = ref
        self.accel = accel
    
    def update(self, dt: float) -> None:
        speed_change = self.speed*self.accel*dt/2
        self.speed += speed_change
        magnitude = self.speed*dt
        move_x, move_y = magnitude*math.cos(self.angle), magnitude*math.sin(self.angle)
        self._ref.x += move_x
        self._ref.y += move_y
        self.speed += speed_change
    

class Gravity(Behavior, Generic[GameObj]):
    def __init__(self, ref:GameObj, accel:float = 9.81, terminal_velo:float|None = None) -> None:
        self.accel = accel
        self.terminal_velo = terminal_velo
        self._ref = ref
    
    def update(self, dt: float) -> None:
        curr_velo = self._ref.velocity_y
        velo_change = -self.accel * dt
        self._ref.velocity_y += velo_change if self.terminal_velo and curr_velo + velo_change > self.terminal_velo else 0
    

class Solid(Behavior):
    solids:set[Type[GameObject]] = set()
    def __init__(self, ref:GameObject) -> None:
        self._ref = ref
        self.__class__.solids.add(type(ref))
        
class JumpThru(Behavior):
    ...



class Focus(Behavior):
    ...










