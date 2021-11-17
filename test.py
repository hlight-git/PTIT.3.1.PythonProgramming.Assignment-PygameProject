import random
from pygame import Vector2
import pygame
class F:
    def __init__(self, tqh):
        self.tqh = Vector2(1, 2)
        self.t = Vector2(self.tqh)
        self.tqh *= 2
    
    def update(self):
        print(1)

class H(F):
    def __init__(self, tqh):
        super().__init__(tqh)

# print(pygame.transform.rotate(Vector2()))