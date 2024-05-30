from typing import Any, TypeVar, Type, Generic

from .player import Player

class GameManager:
    def __init__(self, screen_size:tuple[float, float]) -> None:
        self.screen_size = screen_size
        
        self.game_objects:dict[Any, set[Any]] = {}
        self._objs_to_remove:set[Any] = set()

    def add_object(self, obj):
        """
        Adds the given object `obj` to the appropriate collection in `self.game_objects`.
        """
        if self.game_objects.get(type(obj)):
            self.game_objects[type(obj)].add(obj)
        else:
            self.game_objects[type(obj)] = {obj}
    
    def req_delete_object(self, obj) -> bool:
        """
        Request to delete the given object from the game_objects dictionary. Provides a warning if the object cannot be found.
        
        Args:
            obj (Any): The object to be deleted from the game_objects dictionary.
        
        Returns:
            bool: True if the deletion request was successful, False otherwise.
        """
        if self.game_objects.get(type(obj)) is None:
            print(f"Cannot find object requested to be deleted, {type(obj)} not exist in game_objects.")
            return False
        if obj not in self.game_objects[type(obj)]:
            print(f"Cannot find object requested to be deleted. {obj} not exist in game_objects[{type(obj)}]")
            return False
        return True
            
    def update(self):
        # Handle other game updates
        
        
        for obj_to_rm in self._objs_to_remove:
            self.game_objects[type(obj_to_rm)].remove(obj_to_rm)

    def delete_object(self, obj) -> None:
        """
        Deletes the specified object from the game object manager.
        
        Args:
            obj (Any): The object to be deleted.
        
        Raises:
            KeyError: If the object's type cannot be found in the game object manager, or if the object itself cannot be found in the list of objects for its type.
        """
        if self.game_objects.get(type(obj)) is None:
            raise KeyError(f"Cannot find object to be deleted, {type(obj)} not exist in game_objects.")
        try:
            self.game_objects[type(obj)].remove(obj)
        except KeyError as e:
            raise KeyError(f"Cannot find object to be deleted. {obj} not exist in game_objects[{type(obj)}]")