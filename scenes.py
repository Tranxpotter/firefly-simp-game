import pygame
import pygame_gui
import better_pygame

class Menu(better_pygame.Scene):
    def __init__(self, scene_manager:better_pygame.SceneManager) -> None:
        super().__init__(scene_manager)
        self.scene_manager = scene_manager
        self.screen_size = scene_manager.screen_size
        self.ui_manager = pygame_gui.UIManager(self.screen_size, "themes/menu_theme.json")
        
        self.bg_img = pygame.image.load("assets/menu_bg.png")
        self.bg_img = pygame.transform.scale(self.bg_img, (1280, 720))
        
        self.title = pygame_gui.elements.UILabel(pygame.Rect(0, -100, self.screen_size[0], 200),
                                                 "New Game",
                                                 manager=self.ui_manager,
                                                 anchors={"center":"center"},
                                                 object_id=pygame_gui.core.ObjectID("#title", "@title"))
        
        self.start_btn = pygame_gui.elements.UIButton(pygame.Rect(0, 100, 500, 100),
                                                      "Start",
                                                      self.ui_manager,
                                                      anchors={"center":"center"},
                                                      object_id=pygame_gui.core.ObjectID("#start_btn", "@menu_btn"))
        
        self.settings_btn = pygame_gui.elements.UIButton(pygame.Rect(0, 200, 500, 100),
                                                      "Settings",
                                                      self.ui_manager,
                                                      anchors={"center":"center"},
                                                      object_id=pygame_gui.core.ObjectID("#settings_btn", "@menu_btn"))
        
        self.map_making_btn = pygame_gui.elements.UIButton(pygame.Rect(0, 300, 500, 100),
                                                      "Make map",
                                                      self.ui_manager,
                                                      anchors={"center":"center"},
                                                      object_id=pygame_gui.core.ObjectID("#map_making_btn", "@menu_btn"))
        
    def handle_event(self, event: pygame.Event):
        self.ui_manager.process_events(event)
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_btn:
                self.scene_manager.change_scene("start")
            elif event.ui_element == self.settings_btn:
                self.scene_manager.change_scene("settings")
            elif event.ui_element == self.map_making_btn:
                self.scene_manager.change_scene("map_making")
    
    def update(self, dt: float):
        self.ui_manager.update(dt)
    
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.bg_img, (0, 0))
        self.ui_manager.draw_ui(screen)
    
    