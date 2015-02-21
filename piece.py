import pygame
from pygame import Rect
from pygame import Surface

class Piece(object):
	''' Animated object/ custom sprite stuff.  '''
	def __init__(self, filename, framesperdir, initpos = [0,0],  initdir = None, speed = None, stats = None, id = None, width = 32, height = 64):
		self._images = []
		self._start = pygame.time.get_ticks()
		self._delay = 250
		self._last_update = 0
		self.pos = initpos
		self.speed = speed
		self.moving = False
		self.direction = initdir
		self.framesperdir = framesperdir
		self.animoffset = initdir
		self.frame = 0
		self._lastPos = initpos
		self._lastFacing = initdir
		self.stats = stats
		self.id = id
		self.width = width
		self.height = height		
		self.colrect = pygame.Rect(initpos[0]+2, initpos[1]+36, 30,28)
		# fullrect is for checking full body collision to geometry system
		self.fullrect = pygame.Rect(initpos[0], initpos[1], 32, 64)
		self.exploding_image = pygame.image.load("guts.png").convert()
		self.exploding_image.set_colorkey((0, 0, 0))
		self.exploding = False
		self.exploding_seq = range(1, 640, 4)
		self.exploding_iterator = -1
		self.exploded = False

		#Based on 32x64 sprites
		self.rect = (initpos[0], initpos[1], 32,64)
		image = pygame.image.load(filename).convert()

		for j in range(0, (image.get_height()/64)):
			for i in range(0, (image.get_width()/32)):
				self._images.append(image.subsurface(Rect((i*32, j*32, 32, 64))).convert())
				self._images[len(self._images) - 1].set_colorkey((0, 0, 0))

	def __getitem__(self, key):
		return self.id

	def clear_death(self, hp):
		self.exploded = False
		self.exploding = False
		self.exploding_iterator = -1
		self.stats.hp = hp

	def update(self, direction, redrawOnly = False):
		'''Move the object '''
		#self.direction = direction
		#self.speed = howfast
		if self.stats.hp <= 0:
			self.exploding = True
		if redrawOnly == False:
			if direction == 0:
				self.pos[1] =  self.pos[1] - self.speed
				#self.animoffset = 0
			elif direction == 1:
				self.pos[0] = self.pos[0] - self.speed
				#self.animoffset = 1
			elif direction == 2:
				self.pos[1] = self.pos[1] + self.speed
				#self.animoffset = 2
			elif direction == 3:
				self.pos[0] = self.pos[0] + self.speed
				#self.animoffset = 3

		#Based on 32x64 sprites
		self.rect = (self.pos[0], self.pos[1], 32, 64)
		self.colrect = pygame.Rect(self.pos[0]+8, self.pos[1]+36, 18, 26)

	def draw(self, surface, offsx, offsy):
		self.fullrect = pygame.Rect(self.pos[0] - offsx, self.pos[1] - offsy, 32, 64)
		
		if (self.rect[0]+32 - offsx < 0) or (self.rect[1]+64 - offsy < 0) or (self.rect[0] - offsx > 672) or (self.rect[1] - offsy > 480):
			return
		elif self.exploding == True:
			# still need to touch this up more
			surface.blit(self.exploding_image, (self.rect[0] - offsx - self.exploding_seq[self.exploding_iterator], self.rect[1] - offsy - self.exploding_seq[self.exploding_iterator], self.rect[2], self.rect[3]))
			surface.blit(self.exploding_image, (self.rect[0] - offsx + self.exploding_seq[self.exploding_iterator], self.rect[1] - offsy - self.exploding_seq[self.exploding_iterator], self.rect[2], self.rect[3]))
			surface.blit(self.exploding_image, (self.rect[0] - offsx - self.exploding_seq[self.exploding_iterator], self.rect[1] - offsy + self.exploding_seq[self.exploding_iterator], self.rect[2], self.rect[3]))
			surface.blit(self.exploding_image, (self.rect[0] - offsx + self.exploding_seq[self.exploding_iterator], self.rect[1] - offsy + self.exploding_seq[self.exploding_iterator], self.rect[2], self.rect[3]))
			surface.blit(self.exploding_image, (self.rect[0] - offsx - self.exploding_seq[self.exploding_iterator], self.rect[1] - offsy, self.rect[2], self.rect[3]))
			surface.blit(self.exploding_image, (self.rect[0] - offsx + self.exploding_seq[self.exploding_iterator], self.rect[1] - offsy, self.rect[2], self.rect[3]))
			surface.blit(self.exploding_image, (self.rect[0] - offsx, self.rect[1] - offsy + self.exploding_seq[self.exploding_iterator], self.rect[2], self.rect[3]))
			surface.blit(self.exploding_image, (self.rect[0] - offsx, self.rect[1] - offsy - self.exploding_seq[self.exploding_iterator], self.rect[2], self.rect[3]))


			if(self.exploding_iterator < len(self.exploding_seq) - 1):
				self.exploding_iterator = self.exploding_iterator + 1
			else:
				self.exploded = True
		else:
			t = pygame.time.get_ticks()
			if (t - self._last_update) > self._delay:
				if(self.moving == True):
					self.frame += 1
					self._last_update = t
				elif(self.moving == False):
					self.frame = 1
					self._last_update = t
				if self.frame > self.framesperdir - 1:
					self.frame = 0

			surface.blit(self._images[(self.animoffset*self.framesperdir)+self.frame], (self.rect[0] - offsx, self.rect[1] - offsy, self.rect[2], self.rect[3]))
	
	def set_speed(self, speed):
		self.speed = speed

	def returnToLastPos(self):
		self.direction = self._lastFacing
		self.pos[0] = self._lastPos[0] 
		self.pos[1] = self._lastPos[1]
		self.rect = (self.pos[0], self.pos[1], 32, 64)

	def doesCollide(self, otherPiece):
		if otherPiece.exploding == False:
			if self.colrect.colliderect(otherPiece.colrect):
				return True
			else: 
				return False
		else:
			return False

	def explode(self):
		self.exploding = True

