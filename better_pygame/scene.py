from abc import ABC, abstractmethod

import pygame

from ._constants import ON_TRANSITION_END
from .transition import Transition

class Scene(ABC):
    '''Abstract base class for Scene
    
    Methods
    ----------
    handle_event:
        Used to handle event for the Scene and its elements
    update:
        Called to update the elements inside the Scene with time delta since last call
    draw:
        Called to draw the elements of the Scene onto the screen
    
    Use Example
    --------------
    class TitleScene(Scene):
        def __init__(self):
        
        def handle_event(self, event):
            if event.type == '''
    
    def __init__(self, scene_manager) -> None:
        self.scene_manager = scene_manager
    @abstractmethod
    def handle_event(self, event:pygame.Event):...
    
    @abstractmethod
    def update(self, dt:float):...
    
    @abstractmethod
    def draw(self, screen:pygame.Surface):...
    
    def set_enter_transition(self, transition):
        self._enter_transition = transition
    
    def set_exit_transition(self, transition):
        self._exit_transition = transition
    
    def set_transition_require_update(self, transition_require_update:bool):
        self._transition_require_update = transition_require_update

class SceneManager:
    '''Manager of Scenes
    
    '''
    def __init__(self, screen_size:tuple[int, int], scenes:dict[str, Scene], default_scene:str|None = None, handle_event_during_transition:bool = False) -> None:
        '''
        Initialize Scene Manager, scene_manager will be automatically added to the provided scenes as an attribute (scene._scene_manager)
        Parameters
        -----------
        screen_size: tuple[int, int]
            Defaulted screen size
        scenes: dict[str, Scene]
            Pass in all the scenes and their key as string as identifier
        default_scene: str
            key of the first scene that is selected, if not provided, the first scene provided will be the default
        handle_event_during_transition: bool
            If the scene manager will pass events onto the current scene if a transition is currently running
        '''
        self.screen_size = screen_size
        self.scenes = scenes
        for value in self.scenes.values():
            value.scene_manager = self
        if not default_scene:
            keys = list(scenes.keys())
            if len(keys) > 0:
                self.default_scene = keys[0]
            else:
                self.default_scene = None
        else:
            if default_scene not in scenes.keys():
                raise ValueError(f"Default scene {default_scene} not in scenes")
            self.default_scene = default_scene
        if not self.default_scene:
            self.curr_scene = None
            print("Scene Manager missing default scene.")
        else:
            self.curr_scene = scenes[self.default_scene]
        
        self.prev_scene:Scene|None = None
        self.handle_event_during_transition = handle_event_during_transition
        
        self._transitioning:bool = False
        self._running_transitions:list[Transition] = []
    
    def add_scene(self, key:str, scene:Scene):
        """Add a scene to the manager"""
        if key in self.scenes.keys():
            raise KeyError(f"Scene with key {key} already exists")
        scene.scene_manager = self
        self.scenes[key] = scene
    
    def start_transition(self, transition:Transition, scene:Scene):
        transition.start(scene, self.screen_size)
        self._transitioning = True
        self._running_transitions.append(transition)
    
    def change_scene(self, scene_key:str):
        '''Change to another scene, runs exit and enter transitions
        
        Parameters
        -----------
        scene_key: str
            The key of the scene to switch to'''
        if scene_key not in self.scenes.keys():
            raise ValueError(f"Scene {scene_key} not in scenes")
        self.prev_scene = self.curr_scene
        if self.prev_scene:
            try:
                exit_transition:Transition = self.prev_scene.__getattribute__("_exit_transition")
            except:
                pass
            else:
                self.start_transition(exit_transition, self.prev_scene)
        
        self.curr_scene = self.scenes[scene_key]
        try:
            enter_transition:Transition = self.curr_scene.__getattribute__("_enter_transition")
        except:
            pass
        else:
            self.start_transition(enter_transition, self.curr_scene)
    
    
    def handle_event(self, event:pygame.Event):
        if event.type == ON_TRANSITION_END:
            if event.element in self._running_transitions:
                self._running_transitions.remove(event.element)
                if len(self._running_transitions) == 0:
                    self._transitioning = False
        
        if not self.curr_scene:
            return
        if self._transitioning and not self.handle_event_during_transition:
            return
        self.curr_scene.handle_event(event)
    
    def _transition_get_priority(self, transition:Transition):
        if transition == self.curr_scene:
            return 3
        elif transition == self.prev_scene:
            return 2
        else:
            return 1
    
    def _sort_running_transitions(self):
        self._running_transitions.sort(key=lambda transition: self._transition_get_priority(transition))
    
    def get_transitioning_scenes(self):
        return [t.scene for t in self._running_transitions if t.scene]
    
    def update(self, dt:float):
        if not self.curr_scene:
            return
        curr_scene_transitioning = False
        prev_scene_transitioning = False
        if self._transitioning:
            for transition in self._running_transitions:
                transition.update(dt)
                scene = transition.scene
                if not scene:
                    continue
                try:
                    require_update = scene.__getattribute__("_transition_require_update")
                except:
                    pass
                else:
                    if require_update:
                        scene.update(dt)
                if self.curr_scene == scene:
                    curr_scene_transitioning = True
                elif self.prev_scene == scene:
                    prev_scene_transitioning = True
        
        if not prev_scene_transitioning and self.prev_scene:
            self.prev_scene.update(dt)
        if not curr_scene_transitioning:
            self.curr_scene.update(dt)
    
    def draw(self, screen:pygame.Surface):
        screen.fill((0,0,0))
        if not self.curr_scene:
            return
        
        if self._transitioning:
            transitioning_scenes = self.get_transitioning_scenes()
            if self.prev_scene and self.prev_scene not in transitioning_scenes:
                self.prev_scene.draw(screen)
            if self.curr_scene not in transitioning_scenes:
                self.curr_scene.draw(screen)
                
            for transition in self._running_transitions:
                transition.draw(screen)
            return
        self.curr_scene.draw(screen)
        
       

    
    






