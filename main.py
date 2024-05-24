import pygame
pygame.init()

import better_pygame

def main():
    SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode(SCREEN_SIZE)
    scenes = {}
    
    
    scene_manager = better_pygame.SceneManager(SCREEN_SIZE, scenes)
    
    running = True
    clock = pygame.time.Clock()
    dt = 0
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            scene_manager.handle_event(event)

        scene_manager.update(dt)
        
        scene_manager.draw(screen)
        dt = clock.tick(60)/1000
            






if __name__ == "__main__":
    main()
