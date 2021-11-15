import pygame
from config import *
from script.weapons import *
import math
import random

class Background(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BACKGROUND_LAYER
        self.groups = self.game.all_sprites, self.game.backgrounds
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.image.load('sprites/background/background.png')
        self.image = pygame.transform.scale(self.image, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.padding = 0
    def showing(self):
        if self.rect.x <= - BACKGROUND_WIDTH - SCROLL_LIMIT_HORIZON:
            return False
        if self.rect.x >= CAM_WIDTH + SCROLL_LIMIT_HORIZON:
            return False
        if self.rect.y <= - BACKGROUND_HEIGHT - SCROLL_LIMIT_VERTICAL:
            return False
        if self.rect.y >= CAM_HEIGHT + SCROLL_LIMIT_VERTICAL:
            return False
        return True

    def gen(self, x_gen, y_gen, note):
        for bg in self.game.backgrounds:
            if x_gen == bg.rect.x and y_gen == bg.rect.y:
                return
        # print(f'gen: {note} :', x_gen, y_gen)
        Background(self.game, x_gen, y_gen)
        
    def update(self):
        if not self.showing():
            self.kill()
            return
        if self.rect.x < CAM_WIDTH + SCROLL_LIMIT_HORIZON - BACKGROUND_WIDTH:
            self.gen(self.rect.x + BACKGROUND_WIDTH, self.rect.y, 'right')
            if self.rect.y < CAM_HEIGHT + SCROLL_LIMIT_VERTICAL - BACKGROUND_HEIGHT:
                self.gen(self.rect.x + BACKGROUND_WIDTH, self.rect.y + BACKGROUND_HEIGHT, 'right bot')
            if self.rect.y > -SCROLL_LIMIT_VERTICAL:
                self.gen(self.rect.x + BACKGROUND_WIDTH, self.rect.y - BACKGROUND_HEIGHT, 'right top')
        if self.rect.x > -SCROLL_LIMIT_HORIZON:
            self.gen(self.rect.x - BACKGROUND_WIDTH, self.rect.y, 'left')
            if self.rect.y < CAM_HEIGHT + SCROLL_LIMIT_VERTICAL - BACKGROUND_HEIGHT:
                self.gen(self.rect.x - BACKGROUND_WIDTH, self.rect.y + BACKGROUND_HEIGHT, 'left bot')
            if self.rect.y > -SCROLL_LIMIT_VERTICAL:
                self.gen(self.rect.x - BACKGROUND_WIDTH, self.rect.y - BACKGROUND_HEIGHT, 'left top')
        if self.rect.y < CAM_HEIGHT + SCROLL_LIMIT_VERTICAL - BACKGROUND_HEIGHT:
            self.gen(self.rect.x, self.rect.y + BACKGROUND_HEIGHT, 'bot')
        if self.rect.y > -SCROLL_LIMIT_VERTICAL:
            self.gen(self.rect.x, self.rect.y - BACKGROUND_HEIGHT, 'top')
        
        

class SpriteSheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file)
    
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite
class Player(pygame.sprite.Sprite):
    class ShootingTarget(pygame.sprite.Sprite):
        def __init__(self, game, player):
            self.player = player
            self.game = game
            self._layer = WEAPONS_LAYER
            self.groups = game.all_sprites
            pygame.sprite.Sprite.__init__(self, self.groups)
            
            self.radius = WIN_WIDTH // 40
            self.img = pygame.image.load(f'sprites/ShootingTarget.png')
            self.img = pygame.transform.scale(self.img, (2*self.radius, 2*self.radius))
            self.image = self.img

            self.rect = self.image.get_rect()
            self.moving()

        def moving(self):
            self.rect.center = pygame.mouse.get_pos()

        def resize(self):
            tmp = 30 - self.player.weapon.accuracy//2
            if tmp <= 0:
                self.image = self.img
            else:
                self.image = pygame.transform.scale(self.img, (2*self.radius + tmp, 2*self.radius + tmp))

        def update(self):
            self.moving()
            self.resize()


    def __init__(self, game):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x_change = 0
        self.y_change = 0

        self.facing = 'right'
        self.animation_loop = 0
        self.offset_x = 0
        self.offset_y = 0
        self.speed = PLAYER_SPEED

        img = pygame.image.load(f'sprites/Sunnyland/artwork/Sprites/player/idle/player-idle-1.png')
        img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image = img
        self.mask = pygame.mask.from_surface(img)

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(center = (WIN_WIDTH//2, WIN_HEIGHT//2))

        self.idle_left = []
        for i in range(1, 7):
            img = pygame.image.load(f'sprites/Sunnyland/artwork/Sprites/player/idle/player-idle-{i}.png')
            img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
            img = pygame.transform.flip(img, True, False)
            self.idle_left.append(img)

        self.idle_right = []
        for i in range(1, 7):
            img = pygame.image.load(f'sprites/Sunnyland/artwork/Sprites/player/idle/player-idle-{i}.png')
            img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.idle_right.append(img)
        
        self.move_left = []
        for i in range(1, 7):
            img = pygame.image.load(f'sprites/Sunnyland/artwork/Sprites/player/run/player-run-{i}.png')
            img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
            img = pygame.transform.flip(img, True, False)
            self.move_left.append(img)
            
        self.move_right = []
        for i in range(1, 7):
            img = pygame.image.load(f'sprites/Sunnyland/artwork/Sprites/player/run/player-run-{i}.png')
            img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.move_right.append(img)
        
        self.weapon = ShotGun(self.game, self)
        # self.weapon = AK47(self.game, self)
        self.aim = self.ShootingTarget(self.game, self)

    def aiming(self):
        if pygame.mouse.get_pos()[0] >= self.rect.centerx:
            self.facing = 'right'
        else:
            self.facing = 'left'
    def update(self):
        self.aiming()
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def moving(self):
        return self.x_change != 0 or self.y_change != 0
            
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.offset_x < SCROLL_LIMIT_HORIZON:
                for sprite in self.game.all_sprites:
                    sprite.rect.x += SCROLL_SPEED
                self.offset_x += SCROLL_SPEED
            for sprite in self.game.all_sprites:
                sprite.rect.x += self.speed
            self.x_change -= self.speed
        if keys[pygame.K_d]:
            if -self.offset_x < SCROLL_LIMIT_HORIZON:
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= SCROLL_SPEED
                self.offset_x -= SCROLL_SPEED
            for sprite in self.game.all_sprites:
                sprite.rect.x -= self.speed
            self.x_change += self.speed
        if keys[pygame.K_w]:
            if self.offset_y < SCROLL_LIMIT_VERTICAL:
                for sprite in self.game.all_sprites:
                    sprite.rect.y += SCROLL_SPEED
                self.offset_y += SCROLL_SPEED
            for sprite in self.game.all_sprites:
                sprite.rect.y += self.speed
            self.y_change -= self.speed
        if keys[pygame.K_s]:
            if -self.offset_y < SCROLL_LIMIT_VERTICAL:
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= SCROLL_SPEED
                self.offset_y -= SCROLL_SPEED
            for sprite in self.game.all_sprites:
                sprite.rect.y -= self.speed
            self.y_change += self.speed
        if self.x_change == 0 and self.offset_x != 0:
            sign = self.offset_x/abs(self.offset_x)
            for sprite in self.game.all_sprites:
                sprite.rect.x -= sign*SCROLL_SPEED
            self.offset_x -= sign*SCROLL_SPEED
        if self.y_change == 0 and self.offset_y != 0:
            sign = self.offset_y/abs(self.offset_y)
            for sprite in self.game.all_sprites:
                sprite.rect.y -= sign*SCROLL_SPEED
            self.offset_y -= sign*SCROLL_SPEED
    def animate(self):
        if self.facing == 'left':
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.idle_left[math.floor(self.animation_loop)]
                self.animation_loop += 0.2 * (self.speed/5)
                if self.animation_loop >= len(self.idle_left):
                    self.animation_loop = 0
            else:
                self.image = self.move_left[math.floor(self.animation_loop)]
                self.animation_loop += 0.2 * (self.speed/5)
                if self.animation_loop >= len(self.move_left):
                    self.animation_loop = 0
        if self.facing == 'right':
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.idle_right[math.floor(self.animation_loop)]
                self.animation_loop += 0.2 * (self.speed/5)
                if self.animation_loop >= len(self.idle_right):
                    self.animation_loop = 0
            else:
                self.image = self.move_right[math.floor(self.animation_loop)]
                self.animation_loop += 0.2 * (self.speed/5)
                if self.animation_loop >= len(self.move_right):
                    self.animation_loop = 0