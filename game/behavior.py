from abc import ABC, abstractmethod
import math


class Behavior(ABC):
    @abstractmethod
    def handle_event(self, event) -> None:...
    
    @abstractmethod
    def update(self, dt:float) -> None:...
    
    @abstractmethod
    def draw(self, screen) -> None:...

from .game_object import GameObject

class Anchor(Behavior):
    def handle_event(self, event) -> None:
        ...
        
    def update(self, dt: float) -> None:
        ...
    
    def draw(self, screen) -> None:
        ...

class Projectile(Behavior):
    def __init__(self, speed:float, angle:float, ref:GameObject, accel:float = 0) -> None:
        self.speed = speed
        self.angle = angle
        self._ref = ref
        self.accel = accel
    
    def handle_event(self, event) -> None:
        ...
    
    def update(self, dt: float) -> None:
        speed_change = self.speed*self.accel*dt/2
        self.speed += speed_change
        magnitude = self.speed*dt
        move_x, move_y = magnitude*math.cos(self.angle), magnitude*math.sin(self.angle)
        self._ref.x += move_x
        self._ref.y += move_y
        self.speed += speed_change
    
    def draw(self, screen) -> None:
        ...

class Gravity(Behavior):
    def __init__(self, ref:GameObject, accel:float = 9.81, terminal_velo:float|None = None) -> None:
        self.accel = accel
        self.terminal_velo = terminal_velo
        self._ref = ref
    
    def handle_event(self, event) -> None:
        ...
    
    def update(self, dt: float) -> None:
        curr_velo = self._ref.velocity_y
        velo_change = -self.accel * dt
        self._ref.velocity_y += velo_change if self.terminal_velo and curr_velo + velo_change > self.terminal_velo else 0
    
    def draw(self, screen) -> None:
        ...

class Solid(Behavior):
    def handle_event(self, event) -> None:
        ...
    def update(self, dt: float) -> None:
        ...
    def draw(self, screen) -> None:
        ...

class JumpThru(Behavior):
    def handle_event(self, event) -> None:
        ...
    def update(self, dt: float) -> None:
        ...
    def draw(self, screen) -> None:
        ...



class Focus(Behavior):
    def handle_event(self, event) -> None:
        ...
    def update(self, dt: float) -> None:
        ...
    def draw(self, screen) -> None:
        ...










