from typing import Mapping, TypeVar, Sequence


from .event import Event
from .._typevars import GameObj

class EventManager:
    def __init__(self, events:list[Event], game_manager) -> None:
        self.events = events
        self.game_manager = game_manager
    
    def update(self):
        for event in self.events:
            #Find the suitable objects for the event
            args_type = event.get_event_arguments()
            args = [arg_type.get(self.game_manager) for arg_type in args_type]
            event.run(*args)
        