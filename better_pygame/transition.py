from typing import Literal, Sequence

import pygame

from ._constants import ON_TRANSITION_END
from .utils import *
from .section import Section

class Transition:
    '''Base of all scene transitions
    
    Usage
    ---------
    Initialize the transition object, pass it into a scene's set_start_transition() or set_end_transition() method\n
    To make transition work, Scene.draw() should not be used, instead call Transition.draw(). Transition works by modifying the Surface the Scene drew on.\n
    If Scene is animated, Scene.update() should be called every loop such that the animation will still run during transition.\n
    Do be aware that the Scene's objects coordinates are not moved along with the transition, Scene.handle_event() should not be called while transition is running.\n
    
    Events
    ----------
    on transition end - type: ON_TRANSITION_END, element: Transition, object_id:str|None
    '''
    def __init__(self, sections:Sequence[dict|Section] = [], object_id:str|None = None) -> None:
        '''
        Parameters
        ------------
        sections: list[dict|Section]
            A list of different sections at different durations of the transition
        
        sections dict
        --------------
        A section consist of many things, listed below (`key`: `value_type` - description)\n
        must-have -- `duration`: `int|float` - How long this section lasts\n
        `start_position`: `tuple[int|float, int|float]` - position of the scene at the start of the section\n
        `end_position`: `tuple[int|float, int|float]` - position of the scene at the end of the section\n
        `start_size`: `tuple[int|float, int|float]` - size of the scene at the start of the section\n
        `end_size`: `tuple[int|float, int|float]` - size of the scene at the end of the section\n
        `start_angle`: `int|float` - angle of rotation of the scene at the start of the section\n
        `end_angle`: `int|float` - angle of rotation of the scene at the end of the section, 
            bigger than start for clockwise, smaller than start for anti-clockwise\n
        `rotation_origin`: `tuple[int, int]` - x, y coordinates of the origin of rotation, default is center\n
        `start_transparency`: `int|float` - transparency of the scene at the start of the section, 0-255\n
        `end_transparency`: `int|float` - transparency of the scene at the end of the section, 0-255\n
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


    def start(self, scene, scene_size:tuple[int, int]):
        '''Start the transition for a specific scene
        
        Parameters
        ------------
        scene: `Scene`
            The scene to be transitioned
        scene_size: `tuple`[`int`, `int`]
            The intended screen size for the scene'''
        self.scene = scene
        self.scene_size = scene_size
        self._curr_size = scene_size
        self._running = True
        
        self._on_change_section()
        self._running = True
    
    def terminate(self):
        '''Terminate the running transition and reset all attributes. Triggers ON_TRANSITION_END event.\n
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
        event = pygame.Event(ON_TRANSITION_END, {"element":self, "object_id":self.object_id})
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
                self.__setattr__("_curr_"+attribute+"_change_rate", Transition.get_change_rate_tup(start_val, end_val, duration))
            else:
                self.__setattr__("_curr_"+attribute+"_change_rate", Transition.get_change_rate(start_val, end_val, duration))
        
        
    
    
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
        '''Update transition for each frame'''
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
                event = pygame.Event(ON_TRANSITION_END, {"element":self, "object_id":self.object_id})
                pygame.event.post(event)
            else:
                #Change to next section and update with the remaining unused time of the previous section
                self._on_change_section()
                self.update(dt - section_time)
    
    def draw(self, screen:pygame.Surface):
        '''Draw the transitioning scene on the screen'''
        if not self._running:
            return
        if not self.scene:
            return
        
        surf = transparent_surface(self.scene_size)
        self.scene.draw(surf)
        surf = pygame.transform.scale(surf, self._curr_size)
        surf = pygame.transform.rotate(surf, self._curr_angle % 360)
        
        curr_section = self.sections[self.curr_section_index]
        rotation_origin = curr_section.rotation_origin if isinstance(curr_section, Section) else curr_section.get("rotation_origin")
        if rotation_origin is None:
            #Set rotation origin to center
            rotation_origin = tup_divide(self._curr_size, (2, 2))
        origin_to_size_ratio = tup_divide(rotation_origin, self.scene_size)
        
        rotated_size = surf.get_size()
        if rotated_size != self._curr_size:
            # Reposition the surface to keep rotation origin at center
            position_shift = tup_round(tup_multiply(tup_subtract((rotated_size[0], rotated_size[1]), self._curr_size), origin_to_size_ratio))
        else:
            position_shift = (0,0)
        surf.set_alpha(int(self._curr_transparency))
        screen.blit(surf, tup_subtract(self._curr_position, position_shift))



# def fast_build(screen_size:tuple[int, int], 
#                type:Literal["enter", "exit"], 
#                move_direction:Literal["up", "down", "left", "right", "left-up", "left-down", "right-up", "right-down"]|None,
#                transition_speed:Literal["linear", ""]
#             ):
#     ...

enter_direction_match = {"up":(0, 1), "down":(0, -1), "left":(1, 0), "right":(-1, 0)}
get_enter_start_pos = lambda direction, screen_size: tup_multiply(enter_direction_match[direction], screen_size)

exit_direction_match = {"up":(0, -1), "down":(0, 1), "left":(-1, 0), "right":(1, 0)}
get_exit_end_pos = lambda direction, screen_size: tup_multiply(exit_direction_match[direction], screen_size)

class LinearSlideEnter(Transition):
    def __init__(self, duration, direction:Literal["up", "down", "left", "right"], screen_size:tuple[int, int], object_id: str | None = None) -> None:
        start_pos = get_enter_start_pos(direction, screen_size)
        
        sections = [
            {
                "start_position": start_pos,
                "end_position": (0, 0),
                "duration": duration
            }
        ]
        
        super().__init__(sections, object_id)

class LinearSlideExit(Transition):
    def __init__(self, duration, direction:Literal["up", "down", "left", "right"], screen_size:tuple[int, int], object_id: str | None = None) -> None:
        end_pos = get_exit_end_pos(direction, screen_size)
        
        sections = [
            {
                "start_position": (0, 0),
                "end_position": end_pos,
                "duration": duration
            }
        ]
        
        super().__init__(sections, object_id)


class LinearFadeIn(Transition):
    def __init__(self, duration:float, object_id: str | None = None) -> None:
        sections = [
            {
                "start_transparency": 0,
                "end_transparency": 255,
                "duration": duration
            }
        ]
        super().__init__(sections, object_id)

class LinearFadeOut(Transition):
    def __init__(self, duration:float, object_id: str | None = None) -> None:
        sections = [
            {
                "start_transparency": 255,
                "end_transparency": 0,
                "duration": duration
            }
        ]
        super().__init__(sections, object_id)

class SpinEnter(Transition):
    def __init__(self, duration:float, direction:Literal["up", "down", "left", "right"], screen_size:tuple[int,int], object_id: str | None = None) -> None:
        start_pos = get_enter_start_pos(direction, screen_size)
        sections = [
            {
                "start_position":start_pos,
                "end_position":(0,0),
                "start_angle": 0,
                "end_angle": 360,
                "duration": duration
            }
        ]
        super().__init__(sections, object_id)

class SpinExit(Transition):
    def __init__(self, duration:float, direction:Literal["up", "down", "left", "right"], screen_size:tuple[int,int], object_id: str | None = None) -> None:
        end_pos = get_exit_end_pos(direction, screen_size)
        sections = [
            {
                "start_position":(0, 0),
                "end_position":end_pos,
                "start_angle": 0,
                "end_angle": 360,
                "duration": duration
            }
        ]
        super().__init__(sections, object_id)

class SpinShrinkExit(Transition):
    def __init__(self, duration:float, screen_size:tuple[int,int], object_id: str | None = None) -> None:
        sections = [
            {
                "start_position":(0,0),
                "end_position":(screen_size[0]//2,screen_size[1]//2),
                "start_size":screen_size,
                "end_size":(0,0),
                "start_angle":0,
                "end_angle":360,
                "duration":duration
            }
        ]
        super().__init__(sections, object_id)










