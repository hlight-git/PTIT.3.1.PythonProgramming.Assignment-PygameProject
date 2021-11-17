from config import *
import pygame
import math
import random
import os
from pygame import Vector2
from abc import ABC, abstractclassmethod
from script.items import Icon

class Weapon(ABC):
    def __init__(self, owner):
        self.game = owner.game
        self._layer = WEAPONS_LAYER
        pygame.sprite.Sprite.__init__(self, self.game.interface)
        self.owner = owner
        self.update_time = pygame.time.get_ticks()
        self.backpack = owner.status.backpack
        
        self.animation_list = []
        animation_types = ['Idle', 'Attack']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'sprites/weapons/{self.name}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'sprites/weapons/{self.name}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.flip = False
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.attacking = False
        self.atks = []
        self.rect = owner.rect

    def set_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    @abstractclassmethod
    def attack(self):
        pass

    @abstractclassmethod
    def update_animation(self):
        pass
    
    @abstractclassmethod
    def update_action(self):
        pass

    @abstractclassmethod
    def update(self):
        pass
class Point(pygame.sprite.Sprite):
    def __init__(self, obj, x, y):
        self.obj = obj
        self._layer = 10
        pygame.sprite.Sprite.__init__(self, self.obj.game.interface)
        self.image = pygame.Surface((10,10))
        self.image.fill(RED)
        self.rect = obj.rect
        self.rect.x = x
        self.rect.y = y
class Guns(Weapon):
    def __init__(self, owner):
        self.accuracy = 60
        Weapon.__init__(self, owner)
        num_of_frames = len(os.listdir(f'sprites/weapons/{self.name}/Reload'))
        temp_list = []
        for i in range(num_of_frames):
            img = pygame.image.load(f'sprites/weapons/{self.name}/Reload/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)

    def set_action(self, new_action):
        if self.action == 2:
            if new_action != 2:
                self.owner.speed = PLAYER_SPEED
            else:
                self.owner.speed = PLAYER_SPEED // 2
            self.reload()
        super().set_action(new_action)
  
    def reload(self):
        if self.name == 'ShotGun':
            if not pygame.mixer.Channel(WEAPONS_CHANNEL).get_busy():
                pygame.mixer.Channel(WEAPONS_CHANNEL).play(self.reload_sound[0])
        else:
            if self.backpack.bullets[self.backpack.cur_wp][0] < self.cap_mgz:
                pygame.mixer.Channel(WEAPONS_CHANNEL).play(self.reload_sound)
                    
    def charged(self):
        if self.name == 'ShotGun':
            self.backpack.bullets[self.backpack.cur_wp][1] -= 1
            self.backpack.bullets[self.backpack.cur_wp][0] += 1
        else:
            change = min(self.cap_mgz - self.backpack.bullets[self.backpack.cur_wp][0], self.backpack.bullets[self.backpack.cur_wp][1])
            if change > 0:
                self.backpack.bullets[self.backpack.cur_wp][1] -= change
                self.backpack.bullets[self.backpack.cur_wp][0] += change

    def shoot(self):
        self.atks.append(self.Attack(self))
        if self.name == 'ShotGun':
            self.atks.append(self.Attack(self))
            self.atks.append(self.Attack(self))
        self.attacking = True
        self.backpack.bullets[self.backpack.cur_wp][0] -= 1
        self.shoot_sound.play()
        self.attack_cd = BASE_ATSD * self.aspd

    def attack(self):
        self.set_action(1)
        if self.accuracy > 0:
            self.accuracy -= self.unstable
        self.shoot()

    def update_action(self):
        self.flip = self.owner.flip
        cur_mgz = self.backpack.bullets[self.backpack.cur_wp][0]
        cur_bul_inbp = self.backpack.bullets[self.backpack.cur_wp][1]
        if pygame.key.get_pressed()[pygame.K_r] and (cur_mgz < self.cap_mgz and cur_bul_inbp > 0):
            self.set_action(2)
        mouse_control = pygame.mouse.get_pressed()            
        if mouse_control[0]:
            if self.attack_cd < 0 and cur_mgz > 0:
                self.attack()
        elif mouse_control[2] and (cur_mgz < self.cap_mgz and cur_bul_inbp > 0):
            self.set_action(2)

    def update_animation(self):
        aim_sign = 1
        aim_oAngle = 0
        if self.flip:
            aim_sign = -1
            aim_oAngle = 180
        self.image = pygame.transform.flip(self.animation_list[self.action][self.frame_index], self.flip, False)
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 0:
                    self.frame_index = 0
                elif self.action == 2:
                    self.charged()
                    if self.name == 'ShotGun':
                        reloading = self.backpack.bullets[self.backpack.cur_wp][0] < self.cap_mgz and self.backpack.bullets[self.backpack.cur_wp][1] > 0
                        if reloading:
                            self.frame_index = 0
                            self.reload()
                        else:
                            pygame.mixer.Channel(WEAPONS_CHANNEL).play(self.reload_sound[1])
                            self.set_action(0)
                    else:
                        self.set_action(0)
                else:
                    self.set_action(0)
        if self.action == 2:
            x, y = self.owner.rect.center
            self.rect = self.image.get_rect(center = (x + (aim_sign * self.owner.image.get_width()//6 - 3), y + self.owner.image.get_height()//6))
        else:
            x, y = self.owner.rect.center
            self.rect = self.image.get_rect(center = (x + aim_sign * self.owner.image.get_width()//6 - 3, y + self.owner.image.get_height()//6))
            x_cen, y_cen = self.rect.center
            x, y = pygame.mouse.get_pos()
            arct = math.atan2(y - y_cen, x - x_cen)
            angle = aim_oAngle - math.degrees(arct)
            self.image = pygame.transform.rotate(self.image, angle)
            self.rect = self.image.get_rect(center = (x_cen, y_cen))

    def update(self):
        self.update_action()
        self.update_animation()
        if self.accuracy < 60:
            self.accuracy += 1
        self.attack_cd -= 0.1 * GAME_SPEED
        if self.attack_cd < BASE_ATSD * self.aspd / 1.2:
            self.attacking = False
    class Attack(pygame.sprite.Sprite):
        def __init__(self, weapon):
            self.weapon = weapon
            self._layer = WEAPONS_LAYER
            self.groups = weapon.game.attacks
            self.longevity = weapon.range
            pygame.sprite.Sprite.__init__(self, self.groups)

            dest = pygame.mouse.get_pos()
            src = self.weapon.rect.center
            v = (Vector2(pygame.mouse.get_pos()) - Vector2(self.weapon.rect.center)).normalize() * self.weapon.R
            self.src = self.weapon.rect.center + v
            offset = 30 - self.weapon.accuracy//2
            dir_x = dest[0] - self.src[0] + random.randint(-offset, offset)
            dir_y = dest[1] - self.src[1] + random.randint(-offset, offset)

            self.std_step = Vector2(dir_x, dir_y).normalize()
            self.step = self.std_step * self.weapon.bullet_speed
            self.cur_dis = Vector2()

            img = pygame.transform.scale(weapon.bullet_img, (weapon.bullet_witdh, weapon.bullet_height))
            arct = math.atan2(dir_y, dir_x)
            angle = - math.degrees(arct)
            self.image = pygame.transform.rotate(img, angle)
            self.mask = pygame.mask.from_surface(self.image)

            self.rect = self.image.get_rect(center = src)
            self.hitted_list = []

        def update(self):
            for enemy in self.weapon.game.enemies:
                if pygame.sprite.collide_mask(self, enemy):
                    enemy.hitted_list.append(self)
                    if self.weapon.name != "ShotGun":
                        self.longevity = 0
                        break
            if self.longevity <= 0:
                self.kill()
            else:
                self.longevity -= 0.1
                self.cur_dis += self.step
                self.rect = self.image.get_rect(center = (self.cur_dis + self.src))
class Pistol(Guns, pygame.sprite.Sprite):
    def __init__(self, owner):
        self.name = 'Pistol'
        self.scale = 1.3
        self.bullet_img = pygame.image.load('sprites/bullet2.png')
        self.shoot_sound = pygame.mixer.Sound('sprites/sounds/shoot/pistol.wav')
        self.reload_sound = pygame.mixer.Sound('sprites/sounds/reload/ak47.wav')
        self.bullet_witdh = 15
        self.bullet_height = 5
        self.width = WEAPON_WIDTH
        self.height = WEAPON_HEIGHT
        self.R = self.width//2
        self.unstable = 8
        self.damage = 30
        self.range = 50
        self.cap_mgz = 12
        self.bullet_speed = BULLET_SPEED
        self.push_force = 5
        self.aspd = 0.3
        self.attack_cd = -1
        Guns.__init__(self, owner)

class AR(Guns, pygame.sprite.Sprite):
    def __init__(self, owner):
        Guns.__init__(self, owner)

class AK47(AR):
    def __init__(self, owner):
        self.name = 'AK47'
        self.scale = 3
        self.bullet_img = pygame.image.load('sprites/bullet2.png')
        self.shoot_sound = pygame.mixer.Sound('sprites/sounds/shoot/ak47.wav')
        self.reload_sound = pygame.mixer.Sound('sprites/sounds/reload/ak47.wav')
        self.bullet_witdh = 15
        self.bullet_height = 5
        self.width = WEAPON_WIDTH
        self.height = WEAPON_HEIGHT
        self.R = self.width//2
        self.unstable = 20
        self.damage = 20
        self.range = 50
        self.cap_mgz = 30
        self.bullet_speed = BULLET_SPEED
        self.push_force = 10
        self.aspd = 0.15
        self.attack_cd = -1
        AR.__init__(self, owner)

class M416(AR):
    def __init__(self, owner):
        self.name = 'M416'
        self.scale = 2
        self.bullet_img = pygame.image.load('sprites/bullet2.png')
        self.shoot_sound = pygame.mixer.Sound('sprites/sounds/shoot/m416.wav')
        self.reload_sound = pygame.mixer.Sound('sprites/sounds/reload/ak47.wav')
        self.bullet_witdh = 15
        self.bullet_height = 5
        self.width = WEAPON_WIDTH
        self.height = WEAPON_HEIGHT
        self.R = self.width//2
        self.unstable = 15
        self.damage = 15
        self.range = 50
        self.cap_mgz = 30
        self.bullet_speed = BULLET_SPEED
        self.push_force = 10
        self.aspd = 0.1
        self.attack_cd = -1
        AR.__init__(self, owner)
class ShotGun(Guns, pygame.sprite.Sprite):
    def __init__(self, owner):
        self.scale = 2
        self.bullet_img = pygame.image.load('sprites/bullet2.png')
        self.shoot_sound = pygame.mixer.Sound('sprites/sounds/shoot/shotgun.mp3')
        self.reload_sound = (pygame.mixer.Sound('sprites/sounds/reload/shotgun.mp3'), pygame.mixer.Sound('sprites/sounds/reload/shotgun_done.mp3'))
        self.bullet_witdh = 100
        self.bullet_height = 5
        self.width = WEAPON_WIDTH
        self.height = WEAPON_HEIGHT
        self.R = self.width//2
        self.unstable = 30
        self.damage = 70
        self.range = 0.4
        self.cap_mgz = 7
        self.bullet_speed = BULLET_SPEED*5
        self.push_force = 20
        self.name = 'ShotGun'
        self.aspd = 1
        self.attack_cd = -1
        Guns.__init__(self, owner)