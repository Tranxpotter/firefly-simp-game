from dataclasses import dataclass, field

import pygame

@dataclass
class Player:
    hp:int
    max_hp:int
    base_attack:int
    base_defence:int
    base_shielding:int
    base_speed:int
    position:tuple[int]
    width:int = 20
    height:int = 40
    effects:dict = field(default_factory=dict)
    
    
    
    def handle_event(self, event:pygame.Event):
        pass
    
    
    
    
    

