from typing import Any

from .player import Player

class GameManager:
    def __init__(self, screen_size:tuple[float, float]) -> None:
        self.screen_size = screen_size
        
        self.game_objects:dict[Any, set] = {}

    def add_object(self, obj):
        '''Add obj into game_objects[obj.__class__]'''
        if self.game_objects.get(obj.__class__):
            self.game_objects[obj.__class__].add(obj)
        else:
            self.game_objects[obj.__class__] = {obj}
    
    def delete_object(self, obj):
        '''Delete obj from game_objects[obj.__class__]'''
        if self.game_objects.get(obj.__class__) is None:
            print(f"Cannot find object to be deleted, {obj.__class__} not exist in game_objects.")
        try:
            self.game_objects[obj.__class__].remove(obj)
        except KeyError as e:
            print(f"Cannot find object to be deleted. {obj} not exist in game_objects[{obj.__class__}]")


