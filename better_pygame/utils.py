from typing import TypeVar

import pygame

T = TypeVar("T", int, float)

def tup_add(tup1:tuple[T, T], tup2:tuple[T, T]):
    return tup1[0] + tup2[0], tup1[1] + tup2[1]

def tup_subtract(tup1:tuple[T, T], tup2:tuple[T, T]):
    return tup1[0] - tup2[0], tup1[1] - tup2[1]

def tup_multiply(tup1:tuple[T, T], tup2:tuple[T, T]):
    return tup1[0] * tup2[0], tup1[1] * tup2[1]

def tup_divide(tup1:tuple[T, T], tup2:tuple[T, T]):
    return tup1[0] / tup2[0], tup1[1] / tup2[1]

def tup_absolute(tup:tuple[T, T]):
    return abs(tup[0]), abs(tup[1])

def tup_round(tup:tuple[float, float], decimals:int=0):
    return round(tup[0], decimals), round(tup[1], decimals)

def transparent_surface(size:tuple[T, T]):
    return pygame.Surface(size, pygame.SRCALPHA)