import pygame

ON_ANIMATION_LOOP = pygame.event.custom_type()
ON_ANIMATION_END = pygame.event.custom_type()
ON_TRANSITION_END = pygame.event.custom_type()
ON_EFFECT_END = pygame.event.custom_type()
ON_SECTION_START = pygame.event.custom_type()
ON_SECTION_END = pygame.event.custom_type()

__all__ = [
    "ON_ANIMATION_LOOP",
    "ON_ANIMATION_END",
    "ON_TRANSITION_END"
]