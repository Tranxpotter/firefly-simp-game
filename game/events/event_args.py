from abc import ABC, abstractmethod
from typing import TypeVar, Type, Callable, Tuple, Literal, Any

from ..game_manager import GameManager
from ..game_object import GameObject

GameObj = TypeVar("GameObj", bound=GameObject)

class _EventArgType(ABC):
    @abstractmethod
    def get(self, game_manager:GameManager) -> Any:...
    


class ObjectsArg(_EventArgType):
    def __init__(self, obj_cls:Type[GameObj]) -> None:
        self.obj_cls = obj_cls
    
    def get(self, game_manager: GameManager) -> Any:
        return game_manager.game_objects.get(self.obj_cls, set())

    def __str__(self) -> str:
        return f"set[{self.obj_cls}]"
    







