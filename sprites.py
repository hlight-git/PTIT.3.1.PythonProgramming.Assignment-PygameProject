import pygame
from config import *
import math
import random

class Background(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BACKGROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = WIN_WIDTH
        self.height = WIN_HEIGHT

        self.image = pygame.image.load('sprites/Sunnyland/artwork/Environment/back.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        pass

class SpriteSheet:
    def __init__(self, file):
        super().__init__()
        self.sheet = pygame.image.load(file).convert()
    
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE * PLAYER_SCALE
        self.height = TILESIZE * PLAYER_SCALE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'right'
        self.animation_loop = 0
        self.center_x = 0
        self.center_y = 0

        img = pygame.image.load(f'sprites/Sunnyland/artwork/Sprites/player/idle/player-idle-1.png')
        img = pygame.transform.scale(img, (img.get_width()*PLAYER_SCALE, img.get_height()*PLAYER_SCALE))
        self.image = img

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.idle_left = []
        for i in range(1, 7):
            img = pygame.image.load(f'sprites/Sunnyland/artwork/Sprites/player/idle/player-idle-{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*PLAYER_SCALE, img.get_height()*PLAYER_SCALE))
            img = pygame.transform.flip(img, True, False)
            self.idle_left.append(img)

        self.idle_right = []
        for i in range(1, 7):
            img = pygame.image.load(f'sprites/Sunnyland/artwork/Sprites/player/idle/player-idle-{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*PLAYER_SCALE, img.get_height()*PLAYER_SCALE))
            self.idle_right.append(img)
        
        self.move_left = []
        for i in range(1, 7):
            img = pygame.image.load(f'sprites/Sunnyland/artwork/Sprites/player/run/player-run-{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*PLAYER_SCALE, img.get_height()*PLAYER_SCALE))
            img = pygame.transform.flip(img, True, False)
            self.move_left.append(img)
            
        self.move_right = []
        for i in range(1, 7):
            img = pygame.image.load(f'sprites/Sunnyland/artwork/Sprites/player/run/player-run-{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*PLAYER_SCALE, img.get_height()*PLAYER_SCALE))
            self.move_right.append(img)

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0
    
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.center_x < SCROLL_LIMIT:
                for sprite in self.game.all_sprites:
                    sprite.rect.x += SCROLL_SPEED
                self.center_x += SCROLL_SPEED
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            if -self.center_x < SCROLL_LIMIT:
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= SCROLL_SPEED
                self.center_x -= SCROLL_SPEED
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w]:
            if self.center_y < SCROLL_LIMIT:
                for sprite in self.game.all_sprites:
                    sprite.rect.y += SCROLL_SPEED
                self.center_y += SCROLL_SPEED
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
        if keys[pygame.K_s]:
            if -self.center_y < SCROLL_LIMIT:
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= SCROLL_SPEED
                self.center_y -= SCROLL_SPEED
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
        if sum(keys) == 0:
            if self.center_x != 0:
                sign = self.center_x/abs(self.center_x)
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= sign*SCROLL_SPEED
                self.center_x -= sign*SCROLL_SPEED
            if self.center_y != 0:
                sign = self.center_y/abs(self.center_y)
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= sign*SCROLL_SPEED
                self.center_y -= sign*SCROLL_SPEED
        for sprite in self.game.all_sprites:
            if sprite != self:
                print(sprite.rect.x)
                # print(self.rect.y)
    def animate(self):
        if self.facing == 'left':
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.idle_left[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.idle_left):
                    self.animation_loop = 0
            else:
                self.image = self.move_left[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.move_left):
                    self.animation_loop = 0
        if self.facing == 'right':
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.idle_right[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.idle_right):
                    self.animation_loop = 0
            else:
                self.image = self.move_right[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.move_right):
                    self.animation_loop = 0