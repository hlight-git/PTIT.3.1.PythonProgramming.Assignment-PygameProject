import pygame
from config import *
from abc import ABC, abstractclassmethod
import os

class Enemy(ABC):
    def __init__(self, player, x, y):
        self.player = player
        self.game = player.game
        self._layer = PLAYER_LAYER
        self.groups = player.game.all_sprites, player.game.enemies
        self.update_time = pygame.time.get_ticks()
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_list = []
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
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

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.atk_cd = -1

    def attack(self):
        self.attacking = True
        self.update_new_action(3)
        self.atk_cd = self.atk_speed

    def move(self):
        self.update_new_action(1)
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
            
    def update_new_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_action(self):
        if not self.attacking:
            if pygame.sprite.collide_mask(self, self.player):
                if self.atk_cd <= 0:
                    self.attack()
                else:
                    self.update_new_action(0)
            else:
                self.move()
        for bullet in self.player.game.attacks:
            if pygame.sprite.collide_mask(self, bullet):
                step_back = pygame.Vector2(self.rect.centerx - bullet.rect.centerx, self.rect.centery - bullet.rect.centery).normalize()
                self.rect.center += step_back*100

    def update_animation(self):
        self.image = pygame.transform.flip(self.animation_list[self.action][self.frame_index], self.flip, False)
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.attacking = False
            else:
                self.frame_index = 0

    def update(self):
        self.update_action()
        self.update_animation()
        if self.atk_cd > 0:
            self.atk_cd -= GAME_SPEED


class Covid(Enemy, pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.name = 'enemy'
        self.scale = 2
        self.move_speed = round(ENEMY_SPEED / 5) + 1
        self.atk_speed = ENEMY_SPEED*30
        Enemy.__init__(self, player, x, y)
    # def attack(self):
    #     return super().attack()