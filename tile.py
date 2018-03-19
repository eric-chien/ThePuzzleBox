#Tile class: Tiles are game objects and each have respective images and locations

import pygame

class Tile(pygame.sprite.Sprite):

	def __init__(self, image_file, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.name = image_file
		self.image = pygame.image.load(image_file)
		self.x = x
		self.y = y
		self.rect = self.image.get_rect(topleft=(self.x, self.y))

