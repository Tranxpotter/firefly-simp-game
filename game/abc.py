from abc import ABC, abstractmethod

class Behavior(ABC):
    @abstractmethod
    def handle_event(self, event) -> None:...
    
    @abstractmethod
    def update(self, dt:float) -> None:...
    
    @abstractmethod
    def draw(self, screen) -> None:...