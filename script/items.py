import config
from abc import ABC, abstractclassmethod

class Icon(ABC):
    def __init__(self, x, y):
        super().__init__()
        self.rect.x = x
        self.rect.y = y