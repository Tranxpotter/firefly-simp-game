import pygame

from ._constants import ON_SECTION_START, ON_SECTION_END

class Section:
    '''Represents a Section of a transition or an effect
    
    Events
    -------
    on section start - type: ON_SECTION_START, element: Section, object_id: str|None\n
    on section end - type: ON_SECTION_END, element: Section, object_id: str|None'''
    def __init__(self, 
                 duration:float, 
                 start_position:tuple[float, float]|None = None, 
                 end_position:tuple[float, float]|None = None, 
                 start_size:tuple[float, float]|None = None, 
                 end_size:tuple[float, float]|None = None,
                 start_angle:float|None = None,
                 end_angle:float|None = None,
                 rotation_origin:tuple[int, int]|None = None,
                 start_transparency:float|None = None,
                 end_transparency:float|None = None,
                 object_id:str|None = None
                 ):
        self.duration = duration
        self.start_position = start_position
        self.end_position = end_position
        self.start_size = start_size
        self.end_size = end_size
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.rotation_origin = rotation_origin
        self.start_transparency = start_transparency
        self.end_transparency = end_transparency
        self.object_id = object_id

    def on_start(self):
        """Called when the section starts"""
        event = pygame.Event(ON_SECTION_START, {"element":self, "object_id":self.object_id})
        pygame.event.post(event)
    
    def on_end(self):
        """Called when the section ends"""
        event = pygame.Event(ON_SECTION_END, {"element":self, "object_id":self.object_id})
        pygame.event.post(event)