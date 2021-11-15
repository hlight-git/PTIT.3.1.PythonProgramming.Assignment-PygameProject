from config import *
from abc import ABC, abstractclassmethod

class Icon(ABC):
    def __init__(self, x, y):
        self.rect.x = x
        self.rect.y = y

# class Item(ABC):
#     def __init__(self):
#         self.