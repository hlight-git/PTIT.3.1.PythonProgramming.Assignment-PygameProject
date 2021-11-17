import pygame
from config import *
from script.sprites import *
import sys
class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		pygame.display.set_caption('2m')
		self.clock = pygame.time.Clock()
		self.running = True

	def new(self):
		self.playing = True
		self.pausing = False
		self.cursor_visible = False
		self.time_counter = pygame.time.get_ticks()
		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.backgrounds = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.attacks = pygame.sprite.LayeredUpdates()
		self.interface = pygame.sprite.LayeredUpdates()
		self.player = Player(self)
		Background(self, (WIN_WIDTH - BACKGROUND_WIDTH)//2, (WIN_HEIGHT - BACKGROUND_HEIGHT)//2)
		pygame.mouse.set_visible(self.cursor_visible)
	
	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					self.pausing = not self.pausing
					self.cursor_visible = not self.cursor_visible
					pygame.mouse.set_visible(self.cursor_visible)
				if pygame.K_1 <= event.key <= pygame.K_9:
					self.player.status.backpack.set_weapon(event.key - 48, False)
					
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 4:
					self.player.status.backpack.set_weapon(-1, True)
				elif event.button == 5:
					self.player.status.backpack.set_weapon(1, True)
	def update(self):
		self.time_counter = pygame.time.get_ticks()
		self.all_sprites.update()
		self.attacks.update()
		self.interface.update()

	def draw(self):
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen)
		self.attacks.draw(self.screen)
		self.interface.draw(self.screen)
		self.clock.tick(FPS)
		pygame.display.update()
	
	def win(self):
		self.pausing = True
		
	def lose(self):
		self.playing = False

	def main(self):
		while self.playing:
			self.events()
			if not self.pausing:
				self.update()
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