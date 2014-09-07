import map
from map import *
import pygame
from pygame import *

def draw_map(surface, map, x_offs, y_offs, layer=None):
	''' Draw map at specified x_offs and y_offs '''
	if layer == None:
		for k in range(map.header[5]):
			for j in range(map.header[4]):
				for i in range(map.header[3]):
					if map.data[k][j][i] != 0:
						#if (((i*32)-x_offs)>-32 and ((j*32)-y_offs)>-32 and ((i*32)-x_offs)<672 and ((j*32)-y_offs)<512):
						#if map.tileset[map.data[k][j][i]]:
						surface.blit(map.tileset[map.data[k][j][i]], ((i*32) - x_offs, (j*32) - y_offs))
	else:
		for j in range(map.header[4]):
			for i in range(map.header[3]):
				if map.data[layer][j][i] != 0:
					#if (((i*32)-x_offs)>-32 and ((j*32)-y_offs)>-32 and ((i*32)-x_offs)<672 and ((j*32)-y_offs)<512):
					surface.blit(map.tileset[map.data[layer][j][i]], ((i*32) - x_offs, (j*32) - y_offs))
	
	return surface

class MapRenderer():
	def __init__(self, map):
		self.layers = map.header[5]
		self.map = map
		self.map_surfaces = []
		for z in range(map.header[5]):
			self.map_surfaces.append(pygame.Surface((map.header[3]*32, map.header[4]*32)))

	def prepare_layers(self):
		for z in range(self.layers):
			self.map_surfaces[z] = draw_map(self.map_surfaces[z], self.map, 0, 0, z)
			if(z > 0):
				self.map_surfaces[z].set_colorkey((0, 0, 0))

	def render_layer(self, surface, offs_x, offs_y, layer):
		surface.blit(self.map_surfaces[layer], (-offs_x, -offs_y))
		return surface


