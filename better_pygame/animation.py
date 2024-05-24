import pygame
from ._constants import ON_ANIMATION_END, ON_ANIMATION_LOOP

class Animation:
    '''Simple Animation for an Object
    
        Methods
        ----------------
        update:
            Called every frame to update the Animation object
        get_frame:
            Get the Surface of the current animation frame
        
        Events
        ----------
        Animation loop: type - ON_ANIMATION_LOOP, element - Animation
        Animation end: type - ON_ANIMATION_END, element - Animation
    '''
    
    def __init__(self, images:list[str|pygame.Surface], framerate:int|float, loop:bool = True, loop_count:int = -1, paused:bool = False, object_id:str|None = None) -> None:
        '''
        Parameters
        ----------------------------------------
        images: `list`[`str`|`Surface`]
            A list of pygame Surfaces (recommended) or paths to the images
        framerate: `int`
            Number of frames per second
        loop: `bool`
            If the animation loops
        loop_count: `int`
            The number of times the animation loops, -1 for infinite
        id: `str`
            The id of the object, for handling events
        '''
        self.images:list[pygame.Surface] = []
        for image in images:
            if isinstance(image, str):
                self.images.append(pygame.image.load(image))
            elif isinstance(image, pygame.Surface):
                self.images.append(image)
            else:
                raise ValueError("image must be path string or pygame.Surface")
        
        self.current_frame = 0
        
        self.framerate = framerate
        self.timer = self.frame_delay
        
        self.loop = loop
        self.loop_count = loop_count
        self.curr_loop_count = loop_count
        
        self.paused = paused
        
        self.object_id = object_id
        
        self._running = True
    
    @property
    def frame_delay(self):
        return 1/self.framerate
    
    @frame_delay.setter
    def frame_delay(self, value:float):
        self.framerate = 1/value
    
    def pause(self):
        '''Pause the animation at the current frame'''
        self.paused = True
    
    def resume(self):
        '''Resume paused animation'''
        self.paused = False
    
    def update(self, dt:float):
        '''Called every loop to update the Animation
        
        Parameters
        -------------
        dt: `float`
            Time passed since last frame in seconds'''
        if self.paused or not self._running:
            return
        
        self.timer -= dt
        while self.timer <= 0:
            self.current_frame += 1
            if self.current_frame >= len(self.images):
                if self.loop and self.curr_loop_count > 0:
                    self.current_frame = 0
                    self.curr_loop_count -= 1
                    event = pygame.Event(ON_ANIMATION_LOOP, {"element":self, "object_id":self.object_id})
                    pygame.event.post(event)
                elif self.loop and self.curr_loop_count == -1:
                    self.current_frame = 0
                    event = pygame.Event(ON_ANIMATION_LOOP, {"element":self, "object_id":self.object_id})
                    pygame.event.post(event)
                else:
                    self.current_frame -= 1
                    self._running = False
                    event = pygame.Event(ON_ANIMATION_END, {"element":self, "object_id":self.object_id})
                    pygame.event.post(event)
                    break
            self.timer -= self.frame_delay
    
    def replay(self):
        '''Replay the animation from beginning'''
        self._running = True
        self.timer = self.frame_delay
        self.curr_loop_count = self.loop_count
        self.current_frame = 0
        
    
    def get_frame(self):
        '''Return the Surface for the current frame'''
        return self.images[self.current_frame]


class MultiAnimation:
    '''Used for objects with different switchable animation sequences
    
        Methods
        ----------------
        update:
            Called every frame to update the Animation object
        get_frame:
            Get the Surface of the current animation frame
    '''

    def __init__(self, animations:dict[str, Animation], start:str|None = None) -> None:
        self.animations = animations
        if start and start not in animations.keys():
            raise ValueError(f"Start key {start} not in animations")
        self.curr_animation_key = start
    
    def add_animation(self, key:str, animation:Animation):
        self.animations[key] = animation
    
    def remove_animation(self, key:str):
        if key in self.animations.keys():
            self.animations.pop(key)
        else:
            raise ValueError(f"Key [{key}] not in animations")
    
    def switch_animation(self, key:str):
        if key in self.animations.keys():
            self.curr_animation_key = key
        else:
            raise ValueError(f"Key [{key}] not in animations")
    
    @property
    def curr_animation(self):
        if self.curr_animation_key:
            return self.animations[self.curr_animation_key]
        return None
    
    def update(self, dt:float):
        if not self.curr_animation_key:
            animation_keys = list(self.animations.keys())
            if len(animation_keys) == 0:
                return
            self.curr_animation_key = animation_keys[0]
        
        if self.curr_animation:
            self.curr_animation.update(dt)
    
    def get_frame(self):
        if self.curr_animation:
            return self.curr_animation.get_frame()
        
        
        
        
        





