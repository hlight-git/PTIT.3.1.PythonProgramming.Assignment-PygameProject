import pygame
from config import *
from abc import ABC, abstractclassmethod

class Icon(pygame.sprite.Sprite):
    def __init__(self, game, src, surface, botleft):
        self.game = game
        self.surface = surface
        pygame.sprite.Sprite.__init__(self, game.interface)
        
        self.image = pygame.image.load(src)#.convert()
        scale = 80 / self.image.get_width()
        self.image = pygame.transform.scale(self.image, (int(scale*self.image.get_width()), int(scale*self.image.get_height())))
        self.image = pygame.transform.rotate(self.image, 45)
        self.image.set_alpha(100)
        self.rect = self.image.get_rect(bottomleft = botleft)
    
    def update(self):
        pass

# class Item(ABC):
#     def __init__(self):
#         self.