from config import *
import pygame
from abc import ABC, abstractclassmethod
from script.items import Icon

class Weapon(ABC):
    def __init__(self, game, owner):
        self.game = game
        self.groups = self.game.all_sprites
        self._layer = WEAPONS_LAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.owner = owner

        self.durability = None
        self.unstable = 0

        self.rect.x = self.owner.rect.x
        self.rect.y = self.owner.rect.y

    @abstractclassmethod
    def attack(self, damage):
        pass
    
    def update(self):
        self.rect.x = self.owner.rect.x
        self.rect.y = self.owner.rect.y
        if self.attack_cd < 0:
            mouse_control = pygame.mouse.get_pressed()
            if mouse_control[0]:
                pygame.mixer.Sound("C:/Users/ADMIN/Desktop/2m/sprites/SoundsP/ProjectileShoot.wav").play()
                self.attack_cd = BASE_ATSD * self.aspd
        else:
            self.attack_cd -= 0.1
            # print(self.attack_cd)

        


class Dagger(Weapon, pygame.sprite.Sprite):
    def __init__(self, game, owner):
        self.image = pygame.image.load(f'C:/Users/ADMIN/Desktop/2m/sprites/file deg game 2M/Weapons/Artboard 1.png')
        self.rect = self.image.get_rect()
        Weapon.__init__(self, game, owner)
        self.name = 'Dagger'
        self.damage = None
        self.range = None
        self.aspd = 1
        self.attack_cd = BASE_ATSD * self.aspd
        
    def attack(self, damage):
        return super().attack(damage)
        
class Pistol(Weapon):
    def __init__(self, game, owner):
        Weapon.__init__(game, owner)
        self.name = 'Pistol'

class AR(Weapon):
    def __init__(self, game, owner):
        Weapon.__init__(game, owner)
        self.name = 'AR'
        
class ShotGun(Weapon):
    def __init__(self, game, owner):
        Weapon.__init__(game, owner)
        self.name = 'ShotGun'
        
