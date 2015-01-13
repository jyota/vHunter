# main game concept:
# you are a defender of the undead and monsters for a property
# during the day you set up bombs and other defenses (perhaps with a time limit)
# once time is up or set up is finished, night comes and the
# monster hordes come lurking -- will your defenses protect the family you
# have been hired to protect?
# note: this will take some re-thinking of the engine, currently it's like
# an RPG, moving character with the keyboard. the updated game could easily just
# be something like:
# 1) level intro screen/view level
# 2) purchase items to protect family under a certain budget
# 3) place items for defense
# 4) monsters try to kill the family you were hired to set up defense for
# for each dead monster could be some reward, and potential multiple rounds at a stage to survive
# this requires no player piece to move around, just placement of items.
# family can be on board, but probably just stationary and huddled up in home.
# perhaps they will try to run away if the monsters get close enough or something.

# since partly implemented already, could flesh out the "place items for defense"
# piece first...?
# also, as a prototype, could just do the steps 3 & 4 & assess--
# would start with a 'default' pack of items for the defense for the prototype

import pygame
import gui
from gui import *
import sys
from pygame.locals import *
import mapsave
from mapsave import *
import mapload
from mapload import *
import tiles
from tiles import *
import map
from map import *
import maprender
from maprender import *
import scriptload
from scriptload import *
import scriptsave
from scriptsave import *
import script
from script import *
import piece
from piece import *
import bfs
from bfs import *
import pstats
from pstats import *
import sys
import entities
from entities import *

# Example of calling scripted function
def C_TRIG_TELEPORT_P():
	ourPiece.pos[0] = 360
	return

def C_TRIG_PICKLE_PN():
	if ourPiece.direction == 0:
		print "You got a pickle"
		# test of 'changing tile when pressed
		if ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]][1] == 'C_TRIG_PICKLE_PN':
			print ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]]
			ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)] = 0
		elif ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+28)/32)]][1] == 'C_TRIG_PICKLE_PN':
			print ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]]
			ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+28)/32)] = 0

	return

def C_TRIG_OPEN_DOOR():
	global lastScriptEventTime
	global timeTicks
	global eventDelay

	if(timeTicks - lastScriptEventTime) > eventDelay:
		if ourPiece.direction == 0:
			# test of 'changing tile when pressed
			if ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]][1] == 'C_TRIG_OPEN_DOOR':
				print ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]]
				ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)] = 7
				# Change door tiles after door opened
				ourMap.data[0][((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)] = 2
				ourMap.data[1][(((ourPiece.pos[1]+30)/32))-1][((ourPiece.pos[0]+2)/32)] = 0
				# End change door tiles 
				print "Door Open"
				lastScriptEventTime = timeTicks
			elif ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+28)/32)]][1] == 'C_TRIG_OPEN_DOOR':
				print ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]]
				ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+28)/32)] = 7
				# Change door tiles after door opened
				ourMap.data[0][((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+28)/32)] = 2
				ourMap.data[1][((ourPiece.pos[1]+30)/32)-1][((ourPiece.pos[0]+28)/32)] = 0
				# End change door tiles 
				print "Door Open"
				lastScriptEventTime = timeTicks
		elif ourPiece.direction == 2:
			if ourScript.defs[ourScript.data[((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+2)/32)]][1] == 'C_TRIG_OPEN_DOOR':
				print ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]]
				ourScript.data[((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+2)/32)] = 7
				# Change door tiles after door opened
				ourMap.data[0][((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+2)/32)] = 2
				ourMap.data[1][((ourPiece.pos[1]+66)/32)-1][((ourPiece.pos[0]+2)/32)] = 0
				# End change door tiles 
				print "Door Open"
				lastScriptEventTime = timeTicks
			elif ourScript.defs[ourScript.data[((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+28)/32)]][1] == 'C_TRIG_OPEN_DOOR':
				print ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]]
				ourScript.data[((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+28)/32)] = 7
				# Change door tiles after door opened
				ourMap.data[0][((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+28)/32)] = 2
				ourMap.data[1][((ourPiece.pos[1]+66)/32)-1][((ourPiece.pos[0]+28)/32)] = 0				# End change door tiles 
				print "Door Open"
				lastScriptEventTime = timeTicks

	return

def TRIG_CLOSE_DOOR():
	global lastScriptEventTime
	global timeTicks
	global eventDelay

	if(timeTicks - lastScriptEventTime) > eventDelay:
		if ourPiece.direction == 0:
			# test of 'changing tile when pressed
			if ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]][1] == 'TRIG_CLOSE_DOOR':
				print "Door Close"	
				print ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]]
				ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)] = 6
				# Change door tiles after door closed
				ourMap.data[0][((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)] = 37
				ourMap.data[1][((ourPiece.pos[1]+30)/32)-1][((ourPiece.pos[0]+2)/32)] = 36
				# End change door tiles 
				ourPiece.pos[1] = (((ourPiece.pos[1]+30)/32)*32)
				ourPiece.update(0, True)
				lastScriptEventTime = timeTicks
			elif ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+28)/32)]][1] == 'TRIG_CLOSE_DOOR':
				print "Door Close"	
				print ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+28)/32)]]
				# Change door tiles after door closed
				ourMap.data[0][((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+28)/32)] = 37
				ourMap.data[1][((ourPiece.pos[1]+30)/32)-1][((ourPiece.pos[0]+28)/32)] = 36
				# End change door tiles 
				ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+28)/32)] = 6
				ourPiece.update(0, True)
				ourPiece.pos[1] = (((ourPiece.pos[1]+30)/32)*32)
				lastScriptEventTime = timeTicks
		elif ourPiece.direction == 2:
			# test of 'changing tile when pressed
			lastScriptEventTime = timeTicks
			if ourScript.defs[ourScript.data[((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+2)/32)]][1] == 'TRIG_CLOSE_DOOR':
				print "Door Close"	
				print ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]]
				# Change door tiles after door closed
				ourMap.data[0][((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+2)/32)] = 37
				ourMap.data[1][((ourPiece.pos[1]+66)/32)-1][((ourPiece.pos[0]+2)/32)] = 36
				# End change door tiles 
				ourScript.data[((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+2)/32)] = 6
				ourPiece.pos[1] = (((ourPiece.pos[1]+66)/32)*32)-64
				ourPiece.update(2, True)
				lastScriptEventTime = timeTicks
			elif ourScript.defs[ourScript.data[((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+28)/32)]][1] == 'TRIG_CLOSE_DOOR':
				print "Door Close"	
				print ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]]
				# Change door tiles after door closed
				ourMap.data[0][((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+28)/32)] = 37
				ourMap.data[1][((ourPiece.pos[1]+66)/32)-1][((ourPiece.pos[0]+28)/32)] = 36
				# End change door tiles 
				ourScript.data[((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+28)/32)] = 6
				ourPiece.pos[1] = (((ourPiece.pos[1]+66)/32)*32)-64
				ourPiece.update(2, True)
				lastScriptEventTime = timeTicks

	return

def HPUP():
	ourPiece.stats.hp = ourPiece.stats.hp + 10
	print ourPiece.stats.hp
	return

def HPDOWNP():
	ourPiece.stats.hp = ourPiece.stats.hp - 10
	#print piece.stats.hp
	return

def PLANTED_BOMB():
	# need to add code to remove from tile when goes off
	ourPiece.stats.hp = ourPiece.stats.hp - 100
	return

def render_script_tiles(wheretodraw, script, x_offs, y_offs, tileset):
	for j in range(script.header[2]):
		for i in range(script.header[1]):
			if script.data[j][i] != 0:
				if (((i*32)-x_offs)>-32 and ((j*32)-y_offs)>-32 and ((i*32)-x_offs)<672 and ((j*32)-y_offs)<512):
					wheretodraw.blit(tileset[script.data[j][i]-1], ((i*32) - x_offs, ((j*32) - y_offs)))
	return wheretodraw

def get_text_kb(text_box, wheretodraw):
	''' Stop everything and grab text input and return the value received. '''
	while 1:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					return text_box.value
		wheretodraw.fill((0,0,0,0))
		text_box.update(events)
		text_box.draw(wheretodraw)
		pygame.display.flip()

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
flatten = lambda *n: (e for a in n
    for e in (flatten(*a) if isinstance(a, (tuple, list)) else (a,)))

explosionCircle = list(flatten([range(1, 128, 8), range(128, 1, -4)]))
explosionCircleIteration = 0
screen = pygame.display.set_mode((640, 480), (DOUBLEBUF))
pygame.display.update()
pygame.mouse.set_visible(True)
ourPiece = Piece("testchr.png", 3, [480, 32], 2, 2, PStats(hp = 100), 'PLAYER', 32, 64)
ourEntities = entities()
ourEntities.addEntity(Piece("baddie.png", 3, [320,200], 2, 1, PStats(), 'BADDIE', 32, 64))
ourEntities.addEntity(Piece("baddie.png", 3, [360,260], 2, 1, PStats(), 'BADDIE2', 32, 64))
ourEntities.addEntity(Piece("eilf2b.png", 3, [360,320], 2, 1, PStats(), 'BADDIE2', 32, 64))
ourEntities.addEntity(Piece("baddie.png", 3, [352,200], 2, 1, PStats(), 'BADDIE2', 32, 64))
ourEntities.addEntity(Piece("baddie.png", 3, [352,232], 2, 1, PStats(), 'BADDIE2', 32, 64))

#command line arguments
if(len(sys.argv)>0):
	if(len(sys.argv)==7):
		if(int(sys.argv[3])>5):
			print "Map can only have up to 5 layers. Adjust code if you need more.\n"
			sys.exit()

		ourMap = GameMap("", int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6])
		ourScript = GameScript("", int(sys.argv[1]), int(sys.argv[2]))
		print ourMap.header[2] + "\n"
	elif(len(sys.argv)==2):
		ourMap = GameMap(sys.argv[1])
		ourScript = GameScript(ourMap.header[2])
		print ourMap.header[2] + "\n"
	elif(len(sys.argv)<7):
		print "\nUsage: " + sys.argv[0] + " mapwidth mapheight maplayers tilesetfile mapname mapscript\n\n the above is to create a new map.\n\nTo load a map: " + sys.argv[0] + " mapfilename\n"
		sys.exit()

currentLayer = 0
showDetails = True
showScriptTiles = False
offs_x, offs_y = (0, 0)
currentScript = 0
scriptTiles = []
eventDelay = 750
timeTicks = 0
lastScriptEventTime = 0
map_renderer = MapRenderer(ourMap)
map_renderer.prepare_layers()

for k in range(ourScript.header[0]):
	if k != 0:
		currTile = Surface((32, 32)).convert()
		currTile.fill((0, 255, 255))
		currTile.set_alpha(75)
		gui.draw_text_block(1, 1, currTile, str(k+1))
		print ourScript.defs[k][1]
		scriptTiles.append(currTile)

while 1:

	clock.tick(60) #keep the framerate at 60 or lower
	timeTicks = pygame.time.get_ticks()
	#print clock.get_fps()	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	key=pygame.key.get_pressed()
	if key[pygame.K_q]: 
		sys.exit()
			
	if key[pygame.K_TAB]:
		if(showDetails == True):
			showDetails = False
		else:
			showDetails = True

	if key[pygame.K_z]:
		if(showScriptTiles == True):
			showScriptTiles = False
		else:
			showScriptTiles = True
	
	if(ourPiece.stats.hp <= 0):
		if(explosionCircleIteration == len(explosionCircle) - 1):
			ourPiece.stats.hp = 1000
			explosionCircleIteration = 0
		else:
			explosionCircleIteration = explosionCircleIteration + 1
	else:
		if key[pygame.K_UP]:
			ourPiece.moving = True
			ourPiece.animoffset = 0
			ourPiece.direction = 0
			if ourPiece.pos[1] < -32:
				ourPiece.pos[1] = -32

			if (ourScript.defs[ourScript.data[((ourPiece.pos[1]+33)/32)][((ourPiece.pos[0]+4)/32)]][1].startswith('C') == False) & (ourScript.defs[ourScript.data[((ourPiece.pos[1]+33)/32)][((ourPiece.pos[0]+28)/32)]][1].startswith('C') == False):
				ourPiece.update(0)
				for otherPieces in ourEntities._list:
					if(ourPiece.doesCollide(otherPieces)):
						ourPiece.pos[1] = ourPiece.pos[1] + ourPiece.speed
					break

		if key[pygame.K_LEFT]:
			ourPiece.moving = True
			ourPiece.animoffset = 1
			ourPiece.direction = 1
			if ourPiece.pos[0] < 0:
				ourPiece.pos[0] = 0

			if (ourScript.defs[ourScript.data[((ourPiece.pos[1]+36)/32)][((ourPiece.pos[0])/32)]][1].startswith('C') == False) & (ourScript.defs[ourScript.data[((ourPiece.pos[1]+60)/32)][((ourPiece.pos[0])/32)]][1].startswith('C') == False):
				ourPiece.update(1)
				for otherPieces in ourEntities._list:
					if(ourPiece.doesCollide(otherPieces)):
						ourPiece.pos[0] = ourPiece.pos[0] + ourPiece.speed
					break

		if key[pygame.K_b]:
			# player bomb planting code (toss about 2 tiles away)
			if(ourPiece.direction == 0):
				if(ourScript.data[((ourPiece.pos[1]+32)/32) - 2][((ourPiece.pos[0]+16)/32)] == 0):
					ourScript.data[((ourPiece.pos[1]+32)/32) - 2][((ourPiece.pos[0]+16)/32)] = 8
			if(ourPiece.direction == 1):
				if(ourScript.data[((ourPiece.pos[1]+60)/32)][((ourPiece.pos[0] - 8)/32) - 1] == 0):
					ourScript.data[((ourPiece.pos[1]+60)/32)][((ourPiece.pos[0] - 8)/32) - 1] = 8
			if(ourPiece.direction == 2):
				if(ourScript.data[((ourPiece.pos[1]+60)/32) + 2][((ourPiece.pos[0]+16)/32)] == 0):
					ourScript.data[((ourPiece.pos[1]+60)/32) + 2][((ourPiece.pos[0]+16)/32)] = 8
			if(ourPiece.direction == 3):
				if(ourScript.data[((ourPiece.pos[1]+60)/32)][((ourPiece.pos[0]+40)/32) + 1] == 0):
					ourScript.data[((ourPiece.pos[1]+60)/32)][((ourPiece.pos[0]+40)/32) + 1] = 8

		if key[pygame.K_DOWN]:
			ourPiece.moving = True
			ourPiece.animoffset = 2
			ourPiece.direction = 2
			if ourPiece.pos[1]+65 > ourScript.header[2]*32:
				ourPiece.pos[1] = ourScript.header[2]*32- 65
			elif (ourScript.defs[ourScript.data[((ourPiece.pos[1]+64)/32)][((ourPiece.pos[0]+4)/32)]][1].startswith('C') == False) & (ourScript.defs[ourScript.data[((ourPiece.pos[1]+64)/32)][((ourPiece.pos[0]+28)/32)]][1].startswith('C') == False):
				ourPiece.update(2)
				for otherPieces in ourEntities._list:
					if(ourPiece.doesCollide(otherPieces)):
						ourPiece.pos[1] = ourPiece.pos[1] - ourPiece.speed
					break

		if key[pygame.K_RIGHT]:
			ourPiece.moving = True
			ourPiece.animoffset = 3
			ourPiece.direction = 3
			if ourPiece.pos[0]+33 > ourScript.header[1]*32:
				ourPiece.pos[0] = ourScript.header[2]*32 - 33
			elif (ourScript.defs[ourScript.data[((ourPiece.pos[1]+36)/32)][((ourPiece.pos[0]+32)/32)]][1].startswith('C') == False) & (ourScript.defs[ourScript.data[((ourPiece.pos[1]+60)/32)][((ourPiece.pos[0]+32)/32)]][1].startswith('C') == False):
				ourPiece.update(3)
				for otherPieces in ourEntities._list:
					if(ourPiece.doesCollide(otherPieces)):
						ourPiece.pos[0] = ourPiece.pos[0] - ourPiece.speed
					break

	
		if key[pygame.K_LSHIFT]: 
			ourPiece.speed = 3
		else:
			ourPiece.speed = 2

		if key[pygame.K_RSHIFT]: 
			ourPiece.speed = 1
		
		if key[pygame.K_SPACE]:
			if ourPiece.direction == 0:
				if (ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]][1].find('TRIG') != -1):
				#Example of calling a scripted function
				#if(ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]][1].endswith('N')):
					getattr(sys.modules[__name__], ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+2)/32)]][1])()
					map_renderer = MapRenderer(ourMap)
					map_renderer.prepare_layers()
					
			elif (ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+30)/32)]][1].find('TRIG') != -1):
				#Example of calling a scripted function
				#if (ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+28)/32)]][1].endswith('P')):
					getattr(sys.modules[__name__], ourScript.defs[ourScript.data[((ourPiece.pos[1]+30)/32)][((ourPiece.pos[0]+28)/32)]][1])()
					map_renderer = MapRenderer(ourMap)
					map_renderer.prepare_layers()
					

			if ourPiece.direction == 1:
				if (ourScript.defs[ourScript.data[((ourPiece.pos[1]+36)/32)][((ourPiece.pos[0]-4)/32)]][1].find('TRIG') != -1):
					#Example of calling a scripted function
					#if(ourScript.defs[ourScript.data[((ourPiece.pos[1]+36)/32)][((ourPiece.pos[0]-4)/32)]][1].endswith('P')):
					getattr(sys.modules[__name__], ourScript.defs[ourScript.data[((ourPiece.pos[1]+36)/32)][((ourPiece.pos[0]-4)/32)]][1])() 
					map_renderer = MapRenderer(ourMap)
					map_renderer.prepare_layers()


			elif (ourScript.defs[ourScript.data[((ourPiece.pos[1]+60)/32)][((ourPiece.pos[0]-4)/32)]][1].find('TRIG') != -1):
				#Example of calling a scripted function
				#if(ourScript.defs[ourScript.data[((ourPiece.pos[1]+60)/32)][((ourPiece.pos[0]-4)/32)]][1].endswith('P')):
					getattr(sys.modules[__name__], ourScript.defs[ourScript.data[((ourPiece.pos[1]+60)/32)][((ourPiece.pos[0]-4)/32)]][1])()
					map_renderer = MapRenderer(ourMap)
					map_renderer.prepare_layers()
					
				
			if ourPiece.direction == 2:
				if (ourScript.defs[ourScript.data[((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+2)/32)]][1].find('TRIG') != -1): 
					#Example of calling a scripted function
					#if(ourScript.defs[ourScript.data[((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+2)/32)]][1].endswith('P')):
					getattr(sys.modules[__name__], ourScript.defs[ourScript.data[((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+2)/32)]][1])()
					map_renderer = MapRenderer(ourMap)
					map_renderer.prepare_layers()
					

			elif (ourScript.defs[ourScript.data[((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+31)/32)]][1].find('TRIG') != -1):
				#Example of calling a scripted function
				#if(ourScript.defs[ourScript.data[((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+31)/32)]][1].endswith('P')):
					getattr(sys.modules[__name__], ourScript.defs[ourScript.data[((ourPiece.pos[1]+66)/32)][((ourPiece.pos[0]+31)/32)]][1])()
					map_renderer = MapRenderer(ourMap)
					map_renderer.prepare_layers()
					

			if ourPiece.direction == 3:
				if (ourScript.defs[ourScript.data[((ourPiece.pos[1]+31)/32)][((ourPiece.pos[0]+34)/32)]][1].find('TRIG') != -1):
					#Example of calling a scripted function that affects Player (script item ends with P)
					#if(ourScript.defs[ourScript.data[((ourPiece.pos[1]+31)/32)][((ourPiece.pos[0]+34)/32)]][1].endswith('P')):
					getattr(sys.modules[__name__], ourScript.defs[ourScript.data[((ourPiece.pos[1]+31)/32)][((ourPiece.pos[0]+34)/32)]][1])()
					map_renderer = MapRenderer(ourMap)
					map_renderer.prepare_layers()
					

			elif (ourScript.defs[ourScript.data[((ourPiece.pos[1]+60)/32)][((ourPiece.pos[0]+34)/32)]][1].find('TRIG') != -1):
				#Example of calling a scripted function that affects Player (script item ends with P)
				#if(ourScript.defs[ourScript.data[((ourPiece.pos[1]+60)/32)][((ourPiece.pos[0]+34)/32)]][1].endswith('P')):
					getattr(sys.modules[__name__], ourScript.defs[ourScript.data[((ourPiece.pos[1]+60)/32)][((ourPiece.pos[0]+34)/32)]][1])()
					map_renderer = MapRenderer(ourMap)
					map_renderer.prepare_layers()


		# Call functions for scripted tiles player walks on - determined by points near 'feet' of sprite
		# Precedence goes from left of screen to right, so piece technically can't have two effects happening at once
		# This means, be mindful of this effect when placing walk-on "scripted" tiles adjacent to each other horizontally
		if ourScript.data[((ourPiece.pos[1]+56)/32)][((ourPiece.pos[0]+6)/32)] > 1:
		# Scripted item affects player 
			if "DOOR" not in (ourScript.defs[ourScript.data[((ourPiece.pos[1]+56)/32)][((ourPiece.pos[0]+6)/32)]][1]):
				getattr(sys.modules[__name__], ourScript.defs[ourScript.data[((ourPiece.pos[1]+56)/32)][((ourPiece.pos[0]+6)/32)]][1])()
		elif ourScript.data[((ourPiece.pos[1]+56)/32)][((ourPiece.pos[0]+26)/32)] > 1:
			# Scripted item affects player 
			if "DOOR" not in (ourScript.defs[ourScript.data[((ourPiece.pos[1]+56)/32)][((ourPiece.pos[0]+26)/32)]][1]):
				getattr(sys.modules[__name__], ourScript.defs[ourScript.data[((ourPiece.pos[1]+56)/32)][((ourPiece.pos[0]+26)/32)]][1])()

	#Scrolling map logic
	offs_x = ourPiece.pos[0] - 320
	offs_y = ourPiece.pos[1] - 240
	if(offs_x < 0): offs_x = 0
	if(offs_y < 0): offs_y = 0
	#print ourMap.header[3]*32
	if(ourPiece.pos[0] + 320 > (ourMap.header[3]*32)): offs_x = (ourMap.header[3]*32) - 640
	if(ourPiece.pos[1] + 240 > (ourMap.header[4]*32)): offs_y = (ourMap.header[4]*32) - 480 
	
	screen.fill((0,0,0,0))
	#maprender.draw_map(screen,ourMap,offs_x, offs_y, 0)
	map_renderer.render_layer(screen, offs_x, offs_y, 0)

	# begin entity draw 
	pHasDrawn = 0
	
	for otherEntities in sorted(ourEntities._list, key=lambda entities: entities.pos[1]+64):
		#this moving part is just for testing
		otherEntities.moving = True
		if (otherEntities.pos[0] > ourPiece.pos[0]):
			otherEntities.direction = 1
			otherEntities.animoffset = 1
		else:
			otherEntities.direction = 3
			otherEntities.animoffset = 3

		if (otherEntities.pos[1]+64 > ourPiece.pos[1]+64) & (pHasDrawn == 0):
			ourPiece.draw(screen,offs_x,offs_y)
			otherEntities.draw(screen, offs_x, offs_y)
			
			pHasDrawn = 1
		else:
			otherEntities.draw(screen, offs_x, offs_y)

	if(pHasDrawn==0):
		ourPiece.draw(screen,offs_x,offs_y)
	
	for j in range(1, ourMap.header[5]):
		map_renderer.render_layer(screen, offs_x, offs_y, j)

	ourPiece.moving = False
	if(showDetails == True):
		if(showScriptTiles == True):
			render_script_tiles(screen, ourScript, offs_x, offs_y, scriptTiles)
		screen = gui.draw_text_block(15, 15, screen, "Current Layer: " + str(currentLayer))
		screen = gui.draw_text_block(15, 28, screen, "Current Script Item: " + str(ourScript.defs[currentScript][:]))
		screen = gui.draw_text_block(15, 58, screen, "Current FPS: " + str(clock.get_fps()))

	if(ourPiece.stats.hp <= 0):
		pygame.draw.circle(screen, [255, 0, 0], [ourPiece.pos[0] + 16 - offs_x, ourPiece.pos[1] + 32 - offs_y], explosionCircle[explosionCircleIteration])

	pygame.display.update()
