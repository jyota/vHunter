import pygame, mapload, mapsave, tiles
from pygame import Rect
from mapload import *
from tiles import *

class GameMap:
	def __init__(self, f = "", x = None, y = None, z = None, ts = None, name = None, script = None):
		if f != "":
			self.header, self.data = loadmap(f)
			self.tileset = load_and_cut_tiles(self.header[1])
		elif ts != None:
			self.header = [name, ts, script, x, y, z]
			self.data = [[[0 for k in range(x)] for l in range(y)] for m in range(z)]
			self.tileset = load_and_cut_tiles(self.header[1])
		else:
			self.header = [name, ts, script, x, y, z]
			self.data = [[[0 for k in range(x)] for l in range(y)] for m in range(z)]

	def use_tile_set(self, filename):
		self.header[1] = filename
		self.tileset = load_and_cut_tiles(self.header[1])

	def change_tile_value(self, x, y, z, value):
		self.data[z][y][x] = value

	def get_tile_value(self, x, y, z):
		return self.data[z][y][x]

