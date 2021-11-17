import pygame
import copy
import time

from config import *
# class Player(pygame.sprite.Sprite):
# 	def __init__(self, pos_x, pos_y):
# 		super().__init__()
# 		self.sprites = []
# 		self.is_animating = False
# 		for i in range(1, 6):
# 			img = pygame.image.load(f'sprites/move/right/{i}.png')
# 			img = pygame.transform.scale(img, (img.get_width()//5, img.get_height()//5))
# 			img = pygame.transform.flip(img, True, False)
# 			self.sprites.append(img)
# 		self.curent_sprite = 0
# 		self.image = self.sprites[self.curent_sprite]

# 		self.rect = self.image.get_rect()
# 		self.rect.topleft = [pos_x, pos_y]
	
# 	def animate(self):
# 		self.is_animating = True
# 	def update(self):
# 		if self.is_animating == True:
# 			self.curent_sprite += 0.2
# 			if self.curent_sprite >= len(self.sprites):
# 				self.curent_sprite = 0
# 				self.is_animating = False
# 			self.image = self.sprites[int(self.curent_sprite)]
class Point(pygame.sprite.Sprite):
	def __init__(self, sc, x, y, color, name, enemy):
		self.name = name
		self.sc = sc
		self.image = pygame.Surface((50, 50))
		self.image.fill(RED)
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.enemy = enemy
		self.FONT = pygame.font.SysFont('Futura', 30)
		self.active = True

	def update(self):
		if not self.active:
			return
		if self.name == 'tqh':
			self.rect = self.image.get_rect(center = pygame.mouse.get_pos())
			if pygame.sprite.collide_mask(self, self.enemy):
				self.image.fill((100, 100, 100))
			else:
				self.image.fill((50, 50, 50))
		img = self.FONT.render(f'Bullets: ', True, (123,32,65))
		self.image.blit(img, (0, 0))
		
		self.sc.blit(self.image, self.rect)

pygame.init()
clock = pygame.time.Clock()
# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2m')
img = pygame.image.load('sprites/Sunnyland/artwork/Environment/back.png')
img = pygame.transform.scale(img, (800, 640))
rect = img.get_rect()
enemy = Point(screen, 150, 50, (200, 200, 200), "ble", 1)
player = Point(screen, 0, 0, (255, 0, 0), 'tqh', enemy)
# enemy.active = False
player.active = False

tm = time.time()
p = []
for i in range(5):
	p.append(copy.copy(player))#Point(screen, 0, 0, (255, 0, 0), 'tqh', enemy))
	# p[0].active = True
	# p[i].image.fill((20*i, 20*i, 20*i))
	# for j in range(i):
	# 	p[i].rect.x += 50
	# 	p[i].rect.y += 50
print(len(p))
tm2 = time.time()
print(tm2 - tm)


running = True
while running:
	# screen.blit(img, (0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	screen.fill((255, 255, 255))
	# moving_sprites.draw(screen)
	# moving_sprites.update()
	p[0].update()
	p[1].update()
	p[2].update()
	p[3].update()
	p[4].update()
	# enemy.update()
	player.update()
	pygame.display.update()
	clock.tick(60)

pygame.quit()