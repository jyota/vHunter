import pygame
from pygame import Rect, Surface
import operator

class animated_line():
	def __init__(self, starting_positions, ending_positions, color, width, anim_speed = 0, anim_looping = True, const_offset = [0, 0]):
		self.starting_positions = starting_positions
		self.ending_positions = ending_positions
		self.color = color
		self.width = width
		self.anim_speed = anim_speed
		self.animating = True
		self.anim_looping = anim_looping
		self.const_offset = const_offset
		self.frame = 0
		self.speed_ticker = 0
		self.num_frames = len(starting_positions) 

	def update(self, new_offs):
		if(self.animating == True):
			if(self.speed_ticker == self.anim_speed):
				if (self.num_frames > 0) & (self.frame < (self.num_frames - 1)):
					self.frame = self.frame + 1
				elif self.anim_looping == True:
					self.frame = 0
				elif self.anim_looping == False:
					self.animating = False # stop updates & drawing if not animating
				self.speed_ticker = 0
			elif(self.speed_ticker < self.anim_speed):
				self.speed_ticker = self.speed_ticker + 1
			if new_offs is not None:
				self.const_offset = new_offs

	def draw(self, surface):
		if(self.animating == True):
			pygame.draw.line(surface, self.color, tuple(map(operator.sub, self.starting_positions[self.frame], self.const_offset)), tuple(map(operator.sub, self.ending_positions[self.frame], self.const_offset)), self.width)


