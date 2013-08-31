import pygame, scriptload, scriptsave
from scriptload import *
from scriptsave import *

class GameScript:
	def __init__(self, f = "", x = None, y = None):
		if f != "":
			self.header, self.defs, self.data = loadscript(f)
		else:
			#if script isn't being loaded, fill in defaults. These will need to be updated
			#manually in the raw file.
			self.header = [3, x, y, 'MUSICFILE.MP3']
			self.defs = [[0, 'B', 0], [1, 'C', 1], [2,'FILLER', 2]]
			self.data = [[0 for k in range(self.header[1])] for l in range(self.header[2])]

	def change_script_value(self, x, y, value):
		self.data[y][x] = value

	def get_tile_value(self, x, y):
		return self.data[y][x]

