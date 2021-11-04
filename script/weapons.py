from config import *
import pygame
import math
import random
from pygame import Vector2
from abc import ABC, abstractclassmethod
from script.items import Icon

class Weapon(ABC):
    class Attack(pygame.sprite.Sprite):
        def __init__(self, weapon):
            self.weapon = weapon
            self.damage = 10
            self.range = 10
            self._layer = WEAPONS_LAYER
            self.groups = weapon.game.all_sprites, weapon.game.attacks
            pygame.sprite.Sprite.__init__(self, self.groups)

        def setup(self, src):
            img = pygame.image.load(src)
            img = pygame.transform.scale(img, (10, 10))
            self.image = img

            self.rect = self.image.get_rect(center = self.weapon.get_center())

            dir_x, dir_y = pygame.mouse.get_pos()
            self.src = self.weapon.get_center()
            dir_x = dir_x - self.src[0] + random.randint(-self.weapon.unstable//2, self.weapon.unstable//2)
            dir_y = dir_y - self.src[1] + random.randint(-self.weapon.unstable//2, self.weapon.unstable//2)
            self.step = Vector2(dir_x, dir_y)
            pygame.math.Vector2.normalize_ip(self.step)
            self.step *= BULLET_SPEED
            self.cur_rect = Vector2(self.step)
            self.longevity = self.range
            
        def get_center(self):
            return self.rect.x + 5, self.rect.y + 5

        def update(self):
            if self.longevity <= 0:
                self.kill()
            else:
                self.longevity -= 0.1
                self.cur_rect += self.step
                self.rect = self.image.get_rect(center = (self.cur_rect + self.src))

    def __init__(self, game, owner):
        self.game = game
        self.groups = self.game.all_sprites
        self._layer = WEAPONS_LAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.owner = owner
        self.width = WEAPON_WIDTH
        self.height = WEAPON_HEIGHT
        
        self.right = pygame.transform.scale(self.idle_img, (self.width, self.height))
        self.left = pygame.transform.flip(self.right, True, False)
        self.atk_right = pygame.transform.scale(self.atk_img, (self.width + self.width//4, self.height))
        self.atk_left = pygame.transform.flip(self.atk_right, True, False)

        self.shooting = False
        self.durability = None
        self.unstable = 0
        self.atks = []

        self.rect.x = self.owner.rect.x
        self.rect.y = self.owner.rect.y

    @abstractclassmethod
    def attack(self, damage):
        pass

    def get_center(self):
        return self.rect.x + WEAPON_WIDTH//2, self.rect.y + WEAPON_HEIGHT//2  

    def animate(self):
        aim_sign = 1
        aim_oAngle = 0
        if self.owner.facing == 'left':
            if self.shooting:
                self.image = self.atk_left
            else:
                self.image = self.left
            aim_sign = -1
            aim_oAngle = 180
        else:
            if self.shooting:
                self.image = self.atk_right
            else:
                self.image = self.right
        self.rect.x, self.rect.y = inner_spawn(self, self.owner, aim_sign * self.owner.width//6 - 3, self.owner.height//5 + 7)
        x_cen, y_cen = self.get_center()
        x, y = pygame.mouse.get_pos()
        arct = math.atan2(y - y_cen, x - x_cen)
        self.image = pygame.transform.rotate(self.image, aim_oAngle - math.degrees(arct))
        self.rect = self.image.get_rect(center = (x_cen, y_cen))

    def update(self):
        self.animate()
        mouse_control = pygame.mouse.get_pressed()
        if mouse_control[0]:
            if self.unstable < 60:
                self.unstable += 1
            if self.attack_cd < 0:
                atk = self.Attack(self)
                atk.setup('C:/Users/ADMIN/Desktop/2m/sprites/bullet.png')
                self.atks.append(atk)
                self.shooting = True
                pygame.mixer.Sound("C:/Users/ADMIN/Desktop/2m/sprites/SoundsP/ProjectileShoot.wav").play()
                self.attack_cd = BASE_ATSD * self.aspd
        elif self.unstable > 0:
            self.unstable -= 2
        self.attack_cd -= 0.1 * GAME_SPEED
        if self.attack_cd < BASE_ATSD * self.aspd // 2:
            self.shooting =  False
        


class Dagger(Weapon, pygame.sprite.Sprite):
    def __init__(self, game, owner):
        self.idle_img = pygame.image.load(f'C:/Users/ADMIN/Desktop/2m/sprites/file deg game 2M/Weapons/Artboard 1.png')
        self.rect = self.image.get_rect()
        Weapon.__init__(self, game, owner)
        self.name = 'Dagger'
        self.aspd = 1
        self.attack_cd = BASE_ATSD * self.aspd
        
    def attack(self, damage):
        return super().attack(damage)
        
class Pistol(Weapon, pygame.sprite.Sprite):
    def __init__(self, game, owner):

        Weapon.__init__(self, game, owner)
        self.name = 'Pistol'

class AR(Weapon, pygame.sprite.Sprite):
    def __init__(self, game, owner):
        Weapon.__init__(self, game, owner)
        self.name = 'AR'
        
class ShotGun(Weapon, pygame.sprite.Sprite):
    def __init__(self, game, owner):
        self.idle_img = pygame.image.load(f'C:/Users/ADMIN/Desktop/2m/sprites/R5C6CC4.png')
        self.atk_img = pygame.image.load(f'C:/Users/ADMIN/Desktop/2m/sprites/R5C6CC4s.png')
        self.image = self.idle_img
        self.rect = self.image.get_rect()
        Weapon.__init__(self, game, owner)
        self.name = 'ShotGun'
        self.aspd = 0.15
        self.attack_cd = BASE_ATSD * self.aspd

    def attack(self, damage):
        return super().attack(damage)