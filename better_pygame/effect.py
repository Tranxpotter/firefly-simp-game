from typing import Sequence, Literal, Any
import pygame

from .section import Section
from ._constants import ON_EFFECT_END
from .utils import *
class Effect:
    '''Base of all object Effects
    
    Usage
    ------
    Use as a separate object that is updated every frame and then apply the values to the object it's attached to\n
    Currently object can only be a pygame.Surface\n
    the pygame.Surface should not be drawn while the effect is running, the effect should be drawn instead\n
    if used with pygame_gui objects, the ui_element will be hidden while the effect is running, and back to its original visibility when the effect is done running.\n
    Note that using effect with pygame_gui, the ui_element will need to be image based\n
    
    Events
    ---------
    on effect end - type: ON_EFECT_END, element: Effect, object_id:str|None
    '''
    def __init__(self, sections: Sequence[dict | Section] = [], object_id: str | None = None) -> None:
        '''
        Parameters
        ------------
        sections: list[dict|Section]
            A list of different sections at different durations of the effect
        
        sections dict
        --------------
        A section consist of many things, listed below (`key`: `value_type` - description)\n
        ***ALL THE VALUES HERE SHOULD BE RELATIVE TO THE ORIGINAL VALUES GIVEN***\n
        must-have -- `duration`: `int|float` - How long this section lasts\n
        `start_position`: `tuple[int|float, int|float]` - position of the object at the start of the section\n
        `end_position`: `tuple[int|float, int|float]` - position of the object at the end of the section\n
        `start_size`: `tuple[int|float, int|float]` - size of the object at the start of the section\n
        `end_size`: `tuple[int|float, int|float]` - size of the object at the end of the section\n
        `start_angle`: `int|float` - angle of rotation of the object at the start of the section\n
        `end_angle`: `int|float` - angle of rotation of the object at the end of the section, 
            bigger than start for clockwise, smaller than start for anti-clockwise\n
        `rotation_origin`: `tuple[int, int]` - x, y coordinates of the origin of rotation, default is center\n
        `start_transparency`: `int|float` - transparency of the object at the start of the section, 0-255\n
        `end_transparency`: `int|float` - transparency of the object at the end of the section, 0-255\n
        If any of the start values are omitted, it will default to the previous section end value.\n
        Angles can be bigger than 360, for example, start_angle=0 end_engle=720 gives you 2 clockwise rotations.
        '''
        self.sections = sections
        self.curr_section_index = 0
        self.scene = None
        self.timer = 0
        self._running = False
        
        self._curr_position = (0, 0)
        self._curr_position_change_rate = None
        self._curr_size_change_rate = None
        self._curr_angle = 0
        self._curr_angle_change_rate = None
        self._curr_transparency = 255
        self._curr_transparency_change_rate = None
        
        self.object_id = object_id

    def start(self, image:pygame.Surface, image_position:tuple[float, float], image_size:tuple[float, float], pygame_gui:bool = False, gui_object:Any = None):
        '''Start the effect for an image
        
        Parameters
        -----------
        image: `pygame.Surface`
            The surface of the image to be linked to the effect
        image_position: `tuple[float, float]`
            The original position of the image that will be linked to the effect
        image_size: `tuple[int, int]`
            The original size of the image
        pygame_gui: `bool`
            If the object to be linked to the effect is a pygame_gui object
        gui_object:
            The pygame_gui object that is to be linked to the effect'''
        self._running = True
        self.image = image
        self.original_image_position = image_position
        self._curr_position = image_position
        self.original_image_size = image_size
        self._curr_size = image_size
        
        self._is_pygame_gui = pygame_gui
        if pygame_gui:
            self._gui_object_original_visibility = gui_object.visible
            if self._gui_object_original_visibility == 1:
                gui_object.visible = 0
                
            self._gui_object = gui_object
        
        self._on_change_section()
    
    def set_image(self, image:pygame.Surface):
        '''Update the image with a new image, used for animated objects'''
        self.image = image
        

    def terminate(self):
        '''Terminate the running effect and reset all attributes. Triggers ON_EFFECT_END event.\n
        **Note that ON_SECTION_END will not be triggered'''
        if not self._running:
            return
        self.curr_section_index = 0
        self.scene = None
        self.timer = 0
        self._running = False
        
        self._curr_position = (0, 0)
        self._curr_position_change_rate = None
        self._curr_size_change_rate = None
        self._curr_angle = 0
        self._curr_angle_change_rate = None
        self._curr_transparency = 255
        self._curr_transparency_change_rate = None
        
        if self._is_pygame_gui and self._gui_object_original_visibility:
            self._gui_object.visible = 1
        
        event = pygame.Event(ON_EFFECT_END, {"element":self, "object_id":self.object_id})
        pygame.event.post(event)
    
    
    @staticmethod
    def get_change_rate_tup(start_tup:tuple[int|float, int|float], end_tup:tuple[int|float, int|float], duration:int|float):
        return tup_divide(tup_subtract(end_tup, start_tup), (duration, duration))

    @staticmethod
    def get_change_rate(start_val:int|float, end_val:int|float, duration:int|float):
        return (end_val - start_val) / duration
    
    def _set_change_rate(self, curr_section:dict|Section, attribute:Literal["position","size","angle","transparency"], duration):
        '''Internal set change rate when section changes'''
        if isinstance(curr_section, Section):
            start_val = curr_section.__getattribute__("start_"+attribute)
        else:
            start_val = curr_section.get("start_"+attribute)
        if start_val is None:
            start_val = self.__getattribute__("_curr_"+attribute)
        else:
            self.__setattr__("_curr_"+attribute, start_val)
            
        if isinstance(curr_section, Section):
            end_val = curr_section.__getattribute__("end_"+attribute)
        else:
            end_val = curr_section.get("end_"+attribute)
        if end_val is not None:
            if attribute == "position" or attribute == "size":
                self.__setattr__("_curr_"+attribute+"_change_rate", Effect.get_change_rate_tup(start_val, end_val, duration))
            else:
                self.__setattr__("_curr_"+attribute+"_change_rate", Effect.get_change_rate(start_val, end_val, duration))
        
        
    
    
    def _on_change_section(self):
        '''Internal method called when section changes'''
        curr_section = self.sections[self.curr_section_index]
        
        if isinstance(curr_section, Section):
            self.timer:int|float = curr_section.duration
            duration = curr_section.duration
            curr_section.on_start()
        else:
            self.timer:int|float = curr_section["duration"]
            duration = curr_section["duration"]
        
        if duration is None:
            raise ValueError(f"Duration missing from section, index-{self.curr_section_index}, object_id-{self.object_id}")
        
        #Defaulting current values
        self._curr_position_change_rate = None
        self._curr_size_change_rate = None
        self._curr_angle_change_rate = None
        self._curr_transparency_change_rate = None
        
        # Set change rates for position, size, angle and transparency
        self._set_change_rate(curr_section, "position", duration)
        self._set_change_rate(curr_section, "size", duration)
        self._set_change_rate(curr_section, "angle", duration)
        self._set_change_rate(curr_section, "transparency", duration)
    
    
    def _update_curr_values(self, time:float):
        '''Internal method to update current values based on change rates'''
        if self._curr_position_change_rate:
            self._curr_position = tup_add(self._curr_position, tup_multiply(self._curr_position_change_rate, (time, time)))
        if self._curr_size_change_rate:
            self._curr_size = tup_add(self._curr_size, tup_multiply(self._curr_size_change_rate, (time, time)))
        if self._curr_angle_change_rate:
            self._curr_angle += self._curr_angle_change_rate * time
            if self._curr_angle > 360:
                self._curr_angle -= 360
            elif self._curr_angle < 0:
                self._curr_angle += 360
        if self._curr_transparency_change_rate:
            self._curr_transparency += self._curr_transparency_change_rate * time


    def update(self, dt:float):
        '''Update effect for each frame'''
        if not self._running:
            return
        self.timer -= dt
        if self.timer < 0:
            section_time = self.timer + dt
        else:
            section_time = dt
        self._update_curr_values(section_time)
        
        if self.timer < 0:
            #When current section ends
            curr_section = self.sections[self.curr_section_index]
            if isinstance(curr_section, Section):
                curr_section.on_end()
            self.curr_section_index += 1
            if self.curr_section_index >= len(self.sections):
                #All sections end
                self._running = False
                self.scene = None
                self.curr_section_index -= 1
                event = pygame.Event(ON_EFFECT_END, {"element":self, "object_id":self.object_id})
                pygame.event.post(event)
                if self._is_pygame_gui and self._gui_object_original_visibility:
                    self._gui_object.visible = 1
            else:
                #Change to next section and update with the remaining unused time of the previous section
                self._on_change_section()
                self.update(dt - section_time)


    def draw(self, screen:pygame.Surface):
        '''Draw the effect image on the screen'''
        if not self._running:
            return
        if not self.image:
            return
        surf = transparent_surface(self.original_image_size)
        surf.blit(self.image, (0,0))
        surf = pygame.transform.scale(surf, self._curr_size)
        surf = pygame.transform.rotate(surf, self._curr_angle % 360)
        
        curr_section = self.sections[self.curr_section_index]
        rotation_origin = curr_section.rotation_origin if isinstance(curr_section, Section) else curr_section.get("rotation_origin")
        if rotation_origin is None:
            #Set rotation origin to center
            rotation_origin = tup_divide(self._curr_size, (2, 2))
        origin_to_size_ratio = tup_divide(rotation_origin, self.original_image_size)
        
        rotated_size = surf.get_size()
        if rotated_size != self._curr_size:
            # Reposition the surface to keep rotation origin at center
            position_shift = tup_round(tup_multiply(tup_subtract((rotated_size[0], rotated_size[1]), self._curr_size), origin_to_size_ratio))
        else:
            position_shift = (0,0)
        surf.set_alpha(int(self._curr_transparency))
        screen.blit(surf, tup_add(self.original_image_position, tup_subtract(self._curr_position, position_shift)))
        



class EffectManager:
    ...





















