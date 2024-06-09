from typing import TypeVar
from .abc import Behavior, GameObject


B = TypeVar("B", bound=Behavior)
GameObj = TypeVar("GameObj", bound=GameObject)




