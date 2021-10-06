import pygame


class Player(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y):
		super().__init__()
		self.sprites = []
		self.is_animating = False
		for i in range(1, 6):
			img = pygame.image.load(f'sprites/move/right/{i}.png')
			img = pygame.transform.scale(img, (img.get_width()//5, img.get_height()//5))
			img = pygame.transform.flip(img, True, False)
			self.sprites.append(img)
		self.curent_sprite = 0
		self.image = self.sprites[self.curent_sprite]

		self.rect = self.image.get_rect()
		self.rect.topleft = [pos_x, pos_y]
	
	def animate(self):
		self.is_animating = True
	def update(self):
		if self.is_animating == True:
			self.curent_sprite += 0.2
			if self.curent_sprite >= len(self.sprites):
				self.curent_sprite = 0
				self.is_animating = False
			self.image = self.sprites[int(self.curent_sprite)]
pygame.init()
clock = pygame.time.Clock()
# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2m')
# Background
# x = 200
# y = 200
# img = pygame.image.load('sprites/move/right/1.png')
# img = pygame.transform.scale(img, (img.get_width()//5, img.get_height()//5))
# rect = img.get_rect()
# rect.center = (x, y)
# Player
moving_sprites = pygame.sprite.Group()
player = Player(200, 200)
moving_sprites.add(player)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			moving_right = True
			player.animate()
	
	screen.fill((255, 255, 255))
	moving_sprites.draw(screen)
	moving_sprites.update()
	pygame.display.update()
	clock.tick(60)

pygame.quit()