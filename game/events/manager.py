from typing import Mapping, TypeVar, Sequence


from .event import Event
from game_object import GameObject

GameObj = TypeVar("GameObj", bound=GameObject)
E = TypeVar("E", bound=Event)

class EventManager:
    def __init__(self, events:list[E], game_manager) -> None:
        self.events = events
        self.game_manager = game_manager
    
    def update(self):
        for event in self.events:
            #Find the suitable objects for the event
            pass
            