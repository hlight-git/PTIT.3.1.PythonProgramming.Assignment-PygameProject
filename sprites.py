import pygame
from config import *
from script.weapons import *
from script.enemy import *
import os
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
    class Status(pygame.sprite.Sprite):

        def __init__(self, player):
            self.player = player
            self.max_hp = PLAYER_MAX_HEALTH
            self.hp = self.max_hp
            self.armor = 0
            self.hp_bar = Player.Status.HealthBar(self)
            self.backpack = Player.Status.Backpack(self)

        def take_dame(self, amount):
            if self.armor >= 0:
                self.armor -= amount
            if self.armor < 0:
                self.hp_bar.trans_hp -= self.armor
                self.hp += self.armor
                self.armor = 0
            if self.hp <= 0:
                self.player.game.playing = False
        class HealthBar(pygame.sprite.Sprite):
            def __init__(self, status):
                self.status = status
                self.game = status.player.game
                pygame.sprite.Sprite.__init__(self, self.status.player.game.interface)

                self.bar_width = 250
                self.bar_height = 25
                self.trans_hp = 0
                self.hp_change_speed = 0.2
                self.ratio = self.status.max_hp / self.bar_width
                
                self.image = pygame.Surface((self.bar_width, self.bar_height))
                self.rect = self.image.get_rect()
                self.rect.x = 10
                self.rect.y = 10

            def update(self):
                hp_bar_rect = pygame.Rect(0, 0, self.status.hp/self.ratio, self.bar_height)
                
                self.image.fill(RED)
                pygame.draw.rect(self.image, GREEN, hp_bar_rect)
                if self.status.armor > 0:
                    armor_width = self.status.armor/self.ratio
                    armor_bar_rect = pygame.Rect(hp_bar_rect.right - armor_width, 0, armor_width, self.bar_height)
                    pygame.draw.rect(self.image, CYAN, armor_bar_rect)
                    pygame.draw.rect(self.image, GRAY, (hp_bar_rect.right - armor_width, 0, armor_width, self.bar_height), 1)
                if self.trans_hp > 0:
                    self.trans_hp -= self.hp_change_speed
                    transition_width = int(self.trans_hp/self.ratio)
                    transition_bar_rect = pygame.Rect(hp_bar_rect.right, 0, transition_width, self.bar_height)
                    pygame.draw.rect(self.image, YELLOW, transition_bar_rect)
                pygame.draw.rect(self.image, BLACK, (0, 0, self.bar_width, self.bar_height), 5)

        class Backpack(pygame.sprite.Sprite):
            def __init__(self, status):
                self.status = status
                self.game = status.player.game
                pygame.sprite.Sprite.__init__(self, self.status.player.game.interface)

                self.image = pygame.Surface((250, 50), pygame.SRCALPHA)
                self.rect = self.image.get_rect()
                self.rect.x = 10
                self.rect.y = 50

                self.FONT = pygame.font.SysFont('Futura', 30)
                self.cur_wp = 0
                self.bullets = [[30, 60], [7, 14]]
                self.change_weapon_sound = pygame.mixer.Sound('sprites/sounds/changeGun.wav')
                self.weapon = None

            def set_weapon(self, wp_type, adjacent):
                if wp_type > len(self.bullets) or (self.cur_wp == wp_type - 1 and not adjacent):
                    return
                self.weapon.kill()
                if adjacent:
                    self.cur_wp += wp_type
                    if self.cur_wp < 0:
                        self.cur_wp = len(self.bullets) - 1
                    if self.cur_wp >= len(self.bullets):
                        self.cur_wp = 0
                else:
                    self.cur_wp = wp_type - 1
                pygame.mixer.Channel(WEAPONS_CHANNEL).play(self.change_weapon_sound)
                self.weapon = self.weapon_type(self.cur_wp)

            def weapon_type(self, wt):
                if wt == 0:
                    return AK47(self.status.player)
                if wt == 1:
                    return ShotGun(self.status.player)

            def update(self):
                self.image.fill(EMPTY)
                bullet_sts = self.FONT.render(f'Bullets: {self.bullets[self.cur_wp][0]}/{self.bullets[self.cur_wp][1]}', True, ORANGE)
                self.image.blit(bullet_sts, (0, 0))

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
            tmp = 30 - self.player.status.backpack.weapon.accuracy//2
            if tmp <= 0:
                self.image = self.img
            else:
                self.image = pygame.transform.scale(self.img, (2*self.radius + tmp, 2*self.radius + tmp))

        def update(self):
            self.moving()
            self.resize()


    def __init__(self, game):
        self.game = game
        self.alive = True
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.scale = 2.5
        self.x_change = 0
        self.y_change = 0
        self.update_time = pygame.time.get_ticks()

        self.animation_loop = 0
        self.offset_x = 0
        self.offset_y = 0
        self.speed = PLAYER_SPEED
    
        self.animation_list = []
        animation_types = ['Idle', 'Run', 'IdleHurt', 'RunHurt']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'sprites/player/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'sprites/player/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.idle_left = []
        self.action = 0
        self.flip = False
        self.run_dir = 1
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(center = (WIN_WIDTH//2, WIN_HEIGHT//2))

        self.aim = self.ShootingTarget(self.game, self)
        self.gen_cd = random.randrange(50, 100)
        self.rand_types = []
        for i in range(-1, 2):
            self.rand_types += [(i, -1), (i, 1)]
            if i != 0:
                self.rand_types.append((i, 0))
        self.status = Player.Status(self)
        self.status.backpack.weapon = self.status.backpack.weapon_type(0)

    def aiming(self):
        if pygame.mouse.get_pos()[0] >= self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

    def set_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            if self.run_dir > 0:
                self.frame_index = 0
            else:
                self.frame_index = len(self.animation_list[self.action])-1
            self.update_time = pygame.time.get_ticks()

    def update_action(self):
        if self.x_change != 0 or self.y_change != 0:
            if self.action > 1:
                self.set_action(3)
            else:
                self.set_action(1)
        else:
            if self.action > 1:
                self.set_action(2)
            else:
                self.set_action(0)

    def update_animation(self):
        self.image = pygame.transform.flip(self.animation_list[self.action][self.frame_index], self.flip, False)
        # print(self.action, self.frame_index)
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += self.run_dir
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action > 1:
                self.set_action(self.action - 2)
            else:
                self.frame_index = 0
        elif self.frame_index < 0:
            if self.action > 1:
                self.set_action(self.action - 2)
            else:    
                self.frame_index = len(self.animation_list[self.action]) - 1

    def enemies_gen(self):
        if self.gen_cd > 0:
            self.gen_cd -= GAME_SPEED
        else:
            rt = self.rand_types[random.randint(0, 7)]
            x = random.randrange(rt[0] * WIN_WIDTH, WIN_WIDTH + rt[0] * WIN_WIDTH) + random.randint(100, 400) * rt[0]
            y = random.randrange(rt[1] * WIN_HEIGHT, WIN_HEIGHT + rt[1] * WIN_HEIGHT)
            Enemy(self, x, y)
            self.gen_cd = random.randrange(100, 200)

    def update(self):
        self.aiming()
        self.update_moving()
        self.update_action()
        self.update_animation()
        self.enemies_gen()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0
    
    def update_moving(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if not self.flip:
                self.run_dir = -1
            else:
                self.run_dir = 1
            if self.offset_x < SCROLL_LIMIT_HORIZON:
                for sprite in self.game.all_sprites:
                    sprite.rect.x += SCROLL_SPEED
                self.offset_x += SCROLL_SPEED
            for sprite in self.game.all_sprites:
                sprite.rect.x += self.speed
            self.x_change -= self.speed
        if keys[pygame.K_d]:
            if self.flip:
                self.run_dir = -1
            else:
                self.run_dir = 1
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