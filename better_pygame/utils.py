import pygame

def tup_add(tup1:tuple[int|float, int|float], tup2:tuple[int|float, int|float]):
    return tup1[0] + tup2[0], tup1[1] + tup2[1]

def tup_subtract(tup1:tuple[int|float, int|float], tup2:tuple[int|float, int|float]):
    return tup1[0] - tup2[0], tup1[1] - tup2[1]

def tup_multiply(tup1:tuple[int|float, int|float], tup2:tuple[int|float, int|float]):
    return tup1[0] * tup2[0], tup1[1] * tup2[1]

def tup_divide(tup1:tuple[int|float, int|float], tup2:tuple[int|float, int|float]):
    return tup1[0] / tup2[0], tup1[1] / tup2[1]

def tup_absolute(tup:tuple[int|float, int|float]):
    return abs(tup[0]), abs(tup[1])

def tup_round(tup:tuple[float, float], decimals:int=0):
    return round(tup[0], decimals), round(tup[1], decimals)

def transparent_surface(size:tuple[int|float, int|float]):
    return pygame.Surface(size, pygame.SRCALPHA)