import game
from game.game_object import GameObject
from game.game_manager import GameManager
from game.events.event_args import ObjectsArg


class TestObject(GameObject):
    def __init__(self, game_manager, position: tuple[float, float], size: tuple[float, float], velocity: tuple[float, float] = (0.0, 0.0), properties = []) -> None:
        super().__init__(game_manager, position, size, velocity, properties)

test_obj_arg = ObjectsArg(TestObject)

print(str(test_obj_arg.get_expected_return_type()))
