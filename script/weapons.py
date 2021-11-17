from config import *
import pygame
import math
import random
from pygame import Vector2
from abc import ABC, abstractclassmethod
from script.items import Icon

class Weapon(ABC):
    def __init__(self, owner):
        self.game = owner.game
        self._layer = WEAPONS_LAYER
        pygame.sprite.Sprite.__init__(self, self.game.interface)
        self.owner = owner
        self.backpack = owner.status.backpack
        
        self.animation_list = []
        # animation_types = ['Idle', 'Attack', 'Reload']
        # for animation in animation_types:
        #     temp_list = []
        #     num_of_frames = len(os.listdir(f'sprites/enemies/{self.name}/{animation}'))
        #     for i in range(num_of_frames):
        #         img = pygame.image.load(f'sprites/enemies/{self.name}/{animation}/{i}.png').convert_alpha()
        #         img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
        #         temp_list.append(img)
        #     self.animation_list.append(temp_list)
        self.right = pygame.transform.scale(self.idle_img, (self.width, self.height))
        self.left = pygame.transform.flip(self.right, True, False)
        self.atk_right = pygame.transform.scale(self.atk_img, (self.width, self.height))
        self.atk_left = pygame.transform.flip(self.atk_right, True, False)
        # self.mask = pygame.mask.from_surface(self.image)
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
        pygame.sprite.Sprite.__init__(self, self.obj.game.interface)
        self.image = pygame.Surface((10,10))
        self.image.fill(RED)
        self.rect = obj.rect
    
    def update(self):
        v = (Vector2(pygame.mouse.get_pos()) - Vector2(self.obj.rect.center)).normalize() * self.obj.R
        self.rect = self.image.get_rect(center = (self.obj.rect.center + v))
class Guns(Weapon):
    def __init__(self, owner):
        self.accuracy = 60
        self.reload_right = pygame.transform.scale(self.reload_img, (4*self.width//5, 8*self.height//5))
        self.reload_left = pygame.transform.flip(self.reload_right, True, False)
        self.reloading = False
        Weapon.__init__(self, owner)
        # Point(self)

    def reload(self):
        if self.name == 'ShotGun':
            if not pygame.mixer.Channel(WEAPONS_CHANNEL).get_busy():
                if self.backpack.bullets[self.backpack.cur_wp][0] < self.cap_mgz and self.backpack.bullets[self.backpack.cur_wp][1] > 0:
                    pygame.mixer.Channel(WEAPONS_CHANNEL).play(self.reload_sound[0])
                    self.backpack.bullets[self.backpack.cur_wp][1] -= 1
                    self.backpack.bullets[self.backpack.cur_wp][0] += 1
                else:
                    pygame.mixer.Channel(WEAPONS_CHANNEL).play(self.reload_sound[1])
                    self.reloading = False
                    self.owner.speed = PLAYER_SPEED
        if self.name == 'AR':
            if not pygame.mixer.Channel(WEAPONS_CHANNEL).get_busy():
                if self.backpack.bullets[self.backpack.cur_wp][0] < self.cap_mgz:
                    pygame.mixer.Channel(WEAPONS_CHANNEL).play(self.reload_sound[1])
                    change = min(self.cap_mgz - self.backpack.bullets[self.backpack.cur_wp][0], self.backpack.bullets[self.backpack.cur_wp][1])
                    if change > 0:
                        self.backpack.bullets[self.backpack.cur_wp][1] -= change
                        self.backpack.bullets[self.backpack.cur_wp][0] += change
                self.reloading = False
                self.owner.speed = PLAYER_SPEED

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
        if self.reloading:
            self.reloading = False
            self.owner.speed = PLAYER_SPEED
        if self.accuracy > 0:
            self.accuracy -= self.unstable
        self.shoot()
        
    def animate(self):
        aim_sign = 1
        aim_oAngle = 0
        if self.owner.flip:
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
            self.rect = self.image.get_rect(center = (x + (aim_sign * self.owner.image.get_width()//6 - 3), y + self.owner.image.get_height()//6))
            # self.rect = self.image.get_rect(center = self.owner.rect.center)
        else:
            x, y = self.owner.rect.center
            self.rect = self.image.get_rect(center = (x + aim_sign * self.owner.image.get_width()//6 - 3, y + self.owner.image.get_height()//6))
            # self.rect = self.image.get_rect(center = self.owner.rect.center)
            x_cen, y_cen = self.rect.center
            x, y = pygame.mouse.get_pos()
            arct = math.atan2(y - y_cen, x - x_cen)
            angle = aim_oAngle - math.degrees(arct)
            self.image = pygame.transform.rotate(self.image, angle)
            self.rect = self.image.get_rect(center = (x_cen, y_cen))
        self.game.screen.blit(self.image, (400, 400))

    def update(self):
        self.animate()
        if self.reloading:
            self.reload()
        elif pygame.key.get_pressed()[pygame.K_r]:
            self.reloading = True
            self.owner.speed //= 2
        mouse_control = pygame.mouse.get_pressed()            
        if mouse_control[0]:
            if self.attack_cd < 0 and self.backpack.bullets[self.backpack.cur_wp][0] > 0:
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

            dest = pygame.mouse.get_pos()
            src = self.weapon.rect.center
            v = (Vector2(pygame.mouse.get_pos()) - Vector2(self.weapon.rect.center)).normalize() * self.weapon.R
            src = self.weapon.rect.center + v
            offset = 30 - self.weapon.accuracy//2
            dir_x = dest[0] - src[0] + random.randint(-offset, offset)
            dir_y = dest[1] - src[1] + random.randint(-offset, offset)

            self.std_step = Vector2(dir_x, dir_y).normalize()
            self.step = self.std_step * self.weapon.bullet_speed
            self.cur_dis = Vector2()

            img = pygame.transform.scale(weapon.bullet_img, (weapon.bullet_witdh, weapon.bullet_height))
            arct = math.atan2(dir_y, dir_x)
            angle = - math.degrees(arct)
            self.image = pygame.transform.rotate(img, angle)
            self.mask = pygame.mask.from_surface(self.image)

            self.rect = self.image.get_rect(center = self.weapon.rect.center)
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
                self.rect = self.image.get_rect(center = (self.cur_dis + self.weapon.rect.center))

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
        
# class Pistol(Weapon, pygame.sprite.Sprite):
#     def __init__(self, game, owner):

#         Weapon.__init__(self, game, owner)
#         self.name = 'Pistol'

class AR(Guns, pygame.sprite.Sprite):
    def __init__(self, owner):
        self.name = 'AR'
        Guns.__init__(self, owner)

class AK47(AR):
    def __init__(self, owner):
        self.idle_img = pygame.image.load('sprites/Weapons/Shotgun/Idle/0.png')#.convert()
        self.atk_img = pygame.image.load('sprites/Weapons/Shotgun/Shoot/0.png')#.convert()
        self.reload_img = pygame.image.load('sprites/Weapons/Shotgun/Reload/1.png')
        self.bullet_img = pygame.image.load('sprites/bullet2.png')
        self.shoot_sound = pygame.mixer.Sound('sprites/sounds/shoot/ak47.wav')
        self.reload_sound = (pygame.mixer.Sound('sprites/sounds/reload/shotgun.mp3'), pygame.mixer.Sound('sprites/sounds/reload/shotgun_done.mp3'))
        self.bullet_witdh = 15
        self.bullet_height = 5
        self.width = WEAPON_WIDTH
        self.height = WEAPON_HEIGHT
        self.R = self.width//2
        self.unstable = 16
        self.damage = 30
        self.range = 50
        self.cap_mgz = 30
        self.bullet_speed = BULLET_SPEED
        self.push_force = 10
        self.aspd = 0.1
        self.attack_cd = -1
        AR.__init__(self, owner)
class ShotGun(Guns, pygame.sprite.Sprite):
    def __init__(self, owner):
        self.idle_img = pygame.image.load('sprites/s/Weapons/gun/shotgun/sg1.png')#.convert()
        self.atk_img = pygame.image.load('sprites/s/Weapons/gun/shotgun/sg2.png')#.convert()
        self.reload_img = pygame.image.load('sprites/s/Weapons/gun/shotgun/sgr.png')
        self.bullet_img = pygame.image.load('sprites/bullet2.png')
        self.shoot_sound = pygame.mixer.Sound('sprites/sounds/shoot/shotgun.mp3')
        self.reload_sound = (pygame.mixer.Sound('sprites/sounds/reload/shotgun.mp3'), pygame.mixer.Sound('sprites/sounds/reload/shotgun_done.mp3'))
        self.bullet_witdh = 100
        self.bullet_height = 5
        self.width = WEAPON_WIDTH
        self.height = WEAPON_HEIGHT
        self.R = self.width//2
        self.unstable = 20
        self.damage = 50
        self.range = 0.4
        self.cap_mgz = 7
        self.bullet_speed = BULLET_SPEED*5
        self.push_force = 20
        self.name = 'ShotGun'
        self.aspd = 1
        self.attack_cd = -1
        Guns.__init__(self, owner)