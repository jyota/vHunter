import pygame, os
from pygame import Rect
from pygame import Surface

def load_and_cut_tiles(filename):
	tileGroup = []
	image = pygame.image.load(filename).convert()

	for j in range(0, (image.get_height()/32)):
		for i in range(0, (image.get_width()/32)):
			tileGroup.append(image.subsurface(Rect((i*32, j*32, 32, 32))))
			# Add transparency support for tiles on RGB 0, 0, 0
			tileGroup[len(tileGroup) - 1].set_colorkey((0, 0, 0))

	return tileGroup;
