import pygame
from config import *
from sprites import *
import sys
class Game:
	def __init__(self) -> None:
		pygame.init()
		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		pygame.display.set_caption('2m')
		self.clock = pygame.time.Clock()
		self.running = True

	def new(self):
		self.playing = True
		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.backgrounds = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.attacks = pygame.sprite.LayeredUpdates()

		self.player = Player(self, (WIN_WIDTH - PLAYER_WIDTH)//2, (WIN_HEIGHT - PLAYER_HEIGHT)//2)
		Background(self, (WIN_WIDTH - BACKGROUND_WIDTH)//2, (WIN_HEIGHT - BACKGROUND_HEIGHT)//2)
		# Background(self, 0, 0)
	
	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False
	def update(self):
		self.all_sprites.update()
	def draw(self):
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen)
		self.clock.tick(FPS)
		pygame.display.update()
	def main(self):
		while self.playing:
			self.events()
			self.update()
			print(len(self.backgrounds))
			# for ele in self.backgrounds:
			# 	print(ele.rect.y, end=" ")
			# print()
			self.draw()
		self.running = False

	def game_over(self):
		pass
	def main_menu(self):
		pass

g = Game()
g.main_menu()
g.new()
while g.running:
	g.main()
	g.game_over()

pygame.quit()
sys.exit()