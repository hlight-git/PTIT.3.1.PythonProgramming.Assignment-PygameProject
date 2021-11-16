import pygame
from config import *
from abc import ABC, abstractclassmethod

class Icon(pygame.sprite.Sprite):
    def __init__(self, game, obj):
        self.obj = obj
        self.game = game
        self.image = self.obj.image
        pygame.sprite.Sprite.__init__(self, game.interface)
        # self.image.r

# class Item(ABC):
#     def __init__(self):
#         self.