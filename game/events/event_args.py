from abc import ABC, abstractmethod
from typing import Sequence, TypeVar, Type, Set, Callable, Tuple, Literal, Any, Generic

from ..game_manager import GameManager
from ..game_object import GameObject

GameObj = TypeVar("GameObj", bound=GameObject)

class EventArgument(ABC):
    @abstractmethod
    def get(self, game_manager:GameManager) -> Any:...
    """
    Returns the event arguments for the current game event.
    
    Args:
        game_manager (GameManager): The game manager instance.
    
    Returns:
        Any: The event arguments.
    """
    
    @abstractmethod
    def get_expected_return_type(self) -> Type:...
    """
    Returns the expected return type of the event argument.
    """
    


class ObjectsArg(EventArgument, Generic[GameObj]):
    def __init__(self, obj_cls:Type[GameObj]) -> None:
        self.obj_cls = obj_cls
    
    def get(self, game_manager: GameManager) -> Any:
        """
        Returns the game objects of the specified class from the game manager.
        
        Args:
            game_manager (GameManager): The game manager to retrieve the game objects from.
        
        Returns:
            Any: The game objects of the specified class, or an empty set if none are found.
        """
        return game_manager.game_objects.get(self.obj_cls, set())
    
    def get_expected_return_type(self) -> Type:
        """
        Returns the expected return type for the event object argument.
        """
        return Set[self.obj_cls]

    def __str__(self) -> str:
        return f"set[{self.obj_cls}]"





