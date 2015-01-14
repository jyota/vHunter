import pygame
from pygame import Rect
from pygame import Surface
import AStar

class Piece():
	''' Animated object/ custom sprite stuff.  '''
	def __init__(self, filename, framesperdir, initpos = [0,0],  initdir=None, speed = None, stats = None, id = None, width = 32, height = 64):
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
		self._dest = initpos
		self._path = None
		self._currNode = 0
		self._movementPoints = 0
		self._lastPos = initpos
		self._lastFacing = initdir
		self.stats = stats
		self.id = id
		self.width = width
		self.height = height		
		self.colrect = pygame.Rect(initpos[0]+2, initpos[1]+36, 30,28)
		self.exploding_image = pygame.image.load("guts.png").convert()
		self.exploding_image.set_colorkey((0, 0, 0))
		self.exploding = False
		self.exploding_seq = range(1, 640, 16)
		self.exploding_iterator = -1

		#Based on 32x64 sprites
		self.rect = (initpos[0], initpos[1], 32,64)
		image = pygame.image.load(filename).convert()

		for j in range(0, (image.get_height()/64)):
			for i in range(0, (image.get_width()/32)):
				self._images.append(image.subsurface(Rect((i*32, j*32, 32, 64))).convert())
				self._images[len(self._images) - 1].set_colorkey((0, 0, 0))

	def continue_to_path(self):
		if self.moving == True:
			if self._currNode > len(self._path.nodes)-1 or self._currNode > self._movementPoints-1: 
				self.moving = False
				self._currNode = 0
			elif (self.pos[0] < self._path.nodes[self._currNode].location.x*32):
				self.update(3)
			elif (self.pos[0] > self._path.nodes[self._currNode].location.x*32):
				self.update(1)
			elif (self.pos[1]+32 > self._path.nodes[self._currNode].location.y*32):
				self.update(0)
			elif (self.pos[1]+32 < self._path.nodes[self._currNode].location.y*32):
				self.update(2)
			else: 
				print "Node switch!\n"
				self._currNode += 1

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
		self.colrect = pygame.Rect(self.pos[0]+8, self.pos[1]+36, 18,26)

	def draw(self, surface, offsx, offsy):
		if (self.rect[0]+32 - offsx < 0) or (self.rect[1]+64 - offsy < 0) or (self.rect[0] - offsx > 672) or (self.rect[1] - offsy > 480):
			return
		elif self.exploding == True:
			# still need to touch this up more
			surface.blit(self.exploding_image, (self.rect[0] - offsx - self.exploding_seq[self.exploding_iterator], self.rect[1] - offsy, self.rect[2]  - self.exploding_seq[self.exploding_iterator], self.rect[3]))
			surface.blit(self.exploding_image, (self.rect[0] - offsx - self.exploding_seq[self.exploding_iterator], self.rect[1] - offsy - self.exploding_seq[self.exploding_iterator], self.rect[2], self.rect[3]))
			surface.blit(self.exploding_image, (self.rect[0] - offsx, self.rect[1] - offsy, self.rect[2]  - self.exploding_seq[self.exploding_iterator], self.rect[3]))
			surface.blit(self.exploding_image, (self.rect[0] - offsx, self.rect[1] - offsy + self.exploding_seq[self.exploding_iterator], self.rect[2], self.rect[3]))
			if(self.exploding_iterator < len(self.exploding_seq)):
				self.exploding_iterator = self.exploding_iterator + 1
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

	def set_movement_points(self, mp):
		self._movementPoints = mp
	
	def returnToLastPos(self):
		self.direction = self._lastFacing
		self.pos[0] = self._lastPos[0] 
		self.pos[1] = self._lastPos[1]
		self.rect = (self.pos[0], self.pos[1], 32, 64)

	def moveToTile(self, tilex, tiley, tileColl):
		self._lastPos = [self.pos[0], self.pos[1]]
		self._lastFacing = self.direction

		self._dest = [(tilex*32)/32, (tiley*32)/32]
		if tileColl.data[tiley][tilex] == 1:
			print "Path not found based on tile map.\n"
			return
		astar = AStar.AStar(AStar.SQ_MapHandler(tileColl.data,tileColl.header[1], tileColl.header[2]))
		self._path = astar.findPath(AStar.SQ_Location(self.pos[0]/32, (self.pos[1]+32)/32), AStar.SQ_Location(self._dest[0], self._dest[1]))
		if not self._path:
			print "Path not found.\n"
			self.moving = False
		else:
			print "Path found!\n"
			self.moving = True

	def doesCollide(self, otherPiece):
		if self.colrect.colliderect(otherPiece.colrect):
			return True
		else: 
			return False


