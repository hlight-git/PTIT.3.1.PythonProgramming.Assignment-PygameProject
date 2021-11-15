from config import *
import pygame
import math
import random
from pygame import Vector2
from abc import ABC, abstractclassmethod
from script.items import Icon

class Weapon(ABC):
    def __init__(self, game, owner):
        self.game = game
        self.groups = self.game.all_sprites
        self._layer = WEAPONS_LAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.owner = owner
        
        self.right = pygame.transform.scale(self.idle_img, (self.width, self.height))
        self.left = pygame.transform.flip(self.right, True, False)
        self.atk_right = pygame.transform.scale(self.atk_img, (self.width, self.height))
        self.atk_left = pygame.transform.flip(self.atk_right, True, False)
        self.attacking = False
        self.atks = []
        self.rect = owner.rect

    @abstractclassmethod
    def attack(self):
        pass

    @abstractclassmethod
    def animate(self):
        pass
    
    @abstractclassmethod
    def update(self):
        pass

class Point(pygame.sprite.Sprite):
    def __init__(self, obj):
        self.obj = obj
        self._layer = 10
        pygame.sprite.Sprite.__init__(self, obj.game.all_sprites)
        self.image = pygame.Surface((10,10))
        self.image.fill(RED)
        self.rect = obj.rect
    
    def update(self):
        self.rect = self.image.get_rect(center = self.obj.rect.center)
class Guns(Weapon):
    def __init__(self, game, owner):
        self.accuracy = 60
        self.cur_mgz = self.cap_mgz
        self.reload_right = pygame.transform.scale(self.reload_img, (4*self.width//5, 8*self.height//5))
        self.reload_left = pygame.transform.flip(self.reload_right, True, False)
        self.reloading = False
        Weapon.__init__(self, game, owner)
        Point(self)

    def reload(self):
        if not pygame.mixer.Channel(WEAPONS_CHANNEL).get_busy():
            if self.cur_mgz < self.cap_mgz:
                pygame.mixer.Channel(WEAPONS_CHANNEL).play(self.reload_sound[0])
                self.cur_mgz += 1
            else:
                pygame.mixer.Channel(WEAPONS_CHANNEL).play(self.reload_sound[1])
                self.reloading = False
                self.owner.speed *= 2

    def shoot(self):
        self.atks.append(self.Attack(self))
        self.attacking = True
        self.cur_mgz -= 1
        self.shoot_sound.play()
        self.attack_cd = BASE_ATSD * self.aspd

    def attack(self):
        if self.reloading:
            self.reloading = False
            self.owner.speed *= 2
        if self.accuracy > 0:
            self.accuracy -= self.unstable
        self.shoot()
        
    def animate(self):
        aim_sign = 1
        aim_oAngle = 0
        if self.owner.facing == 'left':
            if self.reloading:
                self.image = self.reload_left
            elif self.attacking:
                self.image = self.atk_left
            else:
                self.image = self.left
            aim_sign = -1
            aim_oAngle = 180
        else:
            if self.reloading:
                self.image = self.reload_right
            elif self.attacking:
                self.image = self.atk_right
            else:
                self.image = self.right
        if self.reloading:
            x, y = self.owner.rect.center
            self.rect = self.image.get_rect(center = (x + (aim_sign * self.owner.image.get_width()//6 - 3), y + self.owner.image.get_height()//5 + 7))
        else:
            x, y = self.owner.rect.center
            self.rect = self.image.get_rect(center = (x + aim_sign * self.owner.image.get_width()//6 - 3, y + self.owner.image.get_height()//5 + 7))
            x_cen, y_cen = self.rect.center
            x, y = pygame.mouse.get_pos()
            arct = math.atan2(y - y_cen, x - x_cen)
            self.image = pygame.transform.rotate(self.image, aim_oAngle - math.degrees(arct))
            self.rect = self.image.get_rect(center = (x_cen, y_cen))

    def update(self):
        self.animate()
        if self.reloading:
            self.reload()
        elif pygame.key.get_pressed()[pygame.K_r]:
            self.reloading = True
            self.owner.speed /= 2
        mouse_control = pygame.mouse.get_pressed()
        if mouse_control[0]:
            if self.attack_cd < 0 and self.cur_mgz > 0:
                self.attack()
        if self.accuracy < 60:
            self.accuracy += 1
        self.attack_cd -= 0.1 * GAME_SPEED
        if self.attack_cd < BASE_ATSD * self.aspd / 1.2:
            self.attacking = False
    class Attack(pygame.sprite.Sprite):
        def __init__(self, weapon):
            self.weapon = weapon
            self._layer = WEAPONS_LAYER
            self.groups = weapon.game.all_sprites, weapon.game.attacks
            self.longevity = weapon.range
            pygame.sprite.Sprite.__init__(self, self.groups)

            img = pygame.transform.scale(weapon.bullet_img, (weapon.bullet_witdh, weapon.bullet_height))
            self.image = img
            self.mask = pygame.mask.from_surface(img)

            self.rect = self.image.get_rect(center = self.weapon.rect.center)

            dir_x, dir_y = pygame.mouse.get_pos()
            offset = 30 - self.weapon.accuracy//2

            self.src = self.weapon.rect.center
            dir_x = dir_x - self.src[0] + random.randint(-offset, offset)
            dir_y = dir_y - self.src[1] + random.randint(-offset, offset)
            self.step = Vector2(dir_x, dir_y).normalize()
            self.step *= self.weapon.bullet_speed
            self.cur_rect = Vector2(self.step)

        def update(self):
            for enemy in self.weapon.game.enemies:
                if pygame.sprite.collide_mask(self, enemy):
                    self.longevity = 0
            if self.longevity <= 0:
                self.kill()
            else:
                self.longevity -= 0.1
                self.cur_rect += self.step
                self.rect = self.image.get_rect(center = (self.cur_rect + self.src))

# class Dagger(Weapon, pygame.sprite.Sprite):
#     def __init__(self, game, owner):
#         self.idle_img = pygame.image.load(f'C:/Users/ADMIN/Desktop/2m/sprites/file deg game 2M/Weapons/Artboard 1.png')
#         self.rect = self.image.get_rect()
#         Weapon.__init__(self, game, owner)
#         self.name = 'Dagger'
#         self.aspd = 1
#         self.attack_cd = BASE_ATSD * self.aspd
        
#     def attack(self, damage):
#         return super().attack(damage)
        
class Pistol(Weapon, pygame.sprite.Sprite):
    def __init__(self, game, owner):

        Weapon.__init__(self, game, owner)
        self.name = 'Pistol'

class AR(Guns, pygame.sprite.Sprite):
    def __init__(self, game, owner):
        self.name = 'AR'
        Guns.__init__(self, game, owner)

class AK47(AR):
    def __init__(self, game, owner):
        self.idle_img = pygame.image.load('C:/Users/ADMIN/Desktop/2m/sprites/s/Weapons/gun/shotgun/sg1.png')#.convert()
        self.atk_img = pygame.image.load('C:/Users/ADMIN/Desktop/2m/sprites/s/Weapons/gun/shotgun/sg2.png')#.convert()
        self.reload_img = pygame.image.load('C:/Users/ADMIN/Desktop/2m/sprites/s/Weapons/gun/shotgun/sgr.png')
        self.bullet_img = pygame.image.load('C:/Users/ADMIN/Desktop/2m/sprites/bullet.png')
        self.shoot_sound = pygame.mixer.Sound('sprites/sounds/shoot/ak47.wav')
        self.reload_sound = (pygame.mixer.Sound('sprites/sounds/reload/shotgun.mp3'), pygame.mixer.Sound('sprites/sounds/reload/shotgun_done.mp3'))
        self.bullet_witdh = 10
        self.bullet_height = 10
        self.width = WEAPON_WIDTH
        self.height = WEAPON_HEIGHT
        self.unstable = 16
        self.damage = 10
        self.range = 5
        self.cap_mgz = 1000
        self.bullet_speed = BULLET_SPEED
        self.aspd = 0.12
        self.attack_cd = -1
        AR.__init__(self, game, owner)
class ShotGun(Guns, pygame.sprite.Sprite):
    def __init__(self, game, owner):
        self.idle_img = pygame.image.load('C:/Users/ADMIN/Desktop/2m/sprites/s/Weapons/gun/shotgun/sg1.png')#.convert()
        self.atk_img = pygame.image.load('C:/Users/ADMIN/Desktop/2m/sprites/s/Weapons/gun/shotgun/sg2.png')#.convert()
        self.reload_img = pygame.image.load('C:/Users/ADMIN/Desktop/2m/sprites/s/Weapons/gun/shotgun/sgr.png')
        self.bullet_img = pygame.image.load('C:/Users/ADMIN/Desktop/2m/sprites/bullet.png')
        self.shoot_sound = pygame.mixer.Sound('C:/Users/ADMIN/Desktop/2m/sprites/sounds/shoot/shotgun.mp3')
        self.reload_sound = (pygame.mixer.Sound('sprites/sounds/reload/shotgun.mp3'), pygame.mixer.Sound('sprites/sounds/reload/shotgun_done.mp3'))
        self.bullet_witdh = 10
        self.bullet_height = 10
        self.width = WEAPON_WIDTH
        self.height = WEAPON_HEIGHT
        self.unstable = 20
        self.damage = 10
        self.range = 1
        self.cap_mgz = 7
        self.bullet_speed = BULLET_SPEED*2
        # self.shoot_reload =
        # self.image = self.idle_img
        # self.rect = self.image.get_rect()
        self.name = 'ShotGun'
        self.aspd = 1
        self.attack_cd = -1
        Guns.__init__(self, game, owner)