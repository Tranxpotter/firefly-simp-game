from abc import ABC, abstractmethod
import pygame

class GameObject(ABC):
    @abstractmethod
    def handle_event(self, event:pygame.Event):...
    
    @abstractmethod
    def update(self, dt:float):...
    
    @abstractmethod
    def draw(self, screen:pygame.Surface):...