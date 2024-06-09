from typing import TypeVar, Type, Callable


from ..abc import Behavior
from .._typevars import GameObj, B



class BehaviorManager:
    def __init__(self) -> None:
        self.behavior_actions:dict[Type[Behavior], Callable] = {}
    
    def add_action(self, cls:Type[Behavior], action:Callable):
        self.behavior_actions[cls] = action

    
















