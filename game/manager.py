from .player import Player

class GameManager:
    def __init__(self, screen_size:tuple[float, float]) -> None:
        self.screen_size = screen_size
        
        self.game_objects = []
        self.player = Player()



