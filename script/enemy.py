import pygame
from config import *
# from abc import ABC, abstractclassmethod
import os
import random
class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.name = 'enemy'
        self.scale = random.randint(3, 3 + min(6, player.game.time_counter//10000))
        self.move_speed = round(ENEMY_SPEED / 5) + 1
        self.atk_speed = ENEMY_SPEED*30
        self.max_hp = 50*self.scale
        self.hp = self.max_hp

        self.player = player
        self.alive = True
        self._layer = PLAYER_LAYER
        self.groups = player.game.all_sprites, player.game.enemies
        self.update_time = pygame.time.get_ticks()
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_list = []
        animation_types = ['Idle', 'Run', 'Attack', 'Dead', 'Hurt']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'sprites/enemies/{self.name}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'sprites/enemies/{self.name}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.action = 1
        self.frame_index = 0
        self.flip = False   
        self.image = self.animation_list[self.action][self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.attacking = False
        self.hitted_list = []

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.damage = 20
        self.atk_cd = -1
        
    def too_far_away(self):
        if abs(self.rect.centerx - self.player.rect.centerx) > 1.5 * BACKGROUND_WIDTH:
            return True
        if abs(self.rect.centery - self.player.rect.centery) > 1.5 * BACKGROUND_HEIGHT:
            return True
        return False

    def attack(self):
        self.attacking = True
        self.set_action(2)
        self.atk_cd = self.atk_speed
        self.player.status.take_dame(self.damage)

    def move(self):
        self.set_action(1)
        if self.rect.centerx < self.player.rect.centerx:
            self.flip = False
            self.rect.centerx += self.move_speed
        elif self.rect.centerx > self.player.rect.centerx:
            self.flip = True
            self.rect.centerx -= self.move_speed
        if self.rect.centery < self.player.rect.centery:
            self.rect.centery += self.move_speed
        elif self.rect.centery > self.player.rect.centery:
            self.rect.centery -= self.move_speed
            
    def set_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_action(self):
        if not self.attacking:
            if pygame.sprite.collide_mask(self, self.player):
                if self.atk_cd <= 0 and self.player.status.hp > 0:
                    self.attack()
                    if self.player.action < 2:
                        self.player.set_action(self.player.action + 2)
                else:
                    self.set_action(0)
            elif self.action != 4:
                self.move()
        if self.hitted_list:
            for hit in self.hitted_list:
                if self not in hit.hitted_list:
                    self.rect.center = self.rect.center + hit.std_step * hit.weapon.push_force
                    self.hp -= hit.weapon.damage
                    hit.hitted_list.append(self)
            self.hitted_list.clear()
            if self.hp <= 0:
                self.alive = False
                self.set_action(3)
            else:
                self.attacking = False
                self.set_action(4)

    def update_animation(self):
        self.image = pygame.transform.flip(self.animation_list[self.action][self.frame_index], self.flip, False)
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.attacking = False
            elif self.action == 3:
                self.kill()
                return
            elif self.action == 4:
                self.set_action(0)
            else:
                self.frame_index = 0

    def update(self):
        if self.alive:
            self.update_action()
            if self.too_far_away():
                self.kill()
                return
        self.update_animation()
        if self.atk_cd > 0:
            self.atk_cd -= GAME_SPEED


# class Covid(Enemy, pygame.sprite.Sprite):
#     def __init__(self, player, x, y):
        
#         Enemy.__init__(self, player, x, y)
#     # def attack(self):
#     #     return super().attack()