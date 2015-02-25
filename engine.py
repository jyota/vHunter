import astar
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
import pstats
from pstats import *
import sys
import entities
from entities import *
import animated_geom
from animated_geom import *
import meter
from meter import *
import geom_draw_system
from geom_draw_system import *
import npc
from npc import *

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

screen = pygame.display.set_mode((640, 480), (DOUBLEBUF))
pygame.display.update()
pygame.mouse.set_visible(True)
ourPiece = Piece("testchr.png", 3, [488, 150], 2, 2, PStats(hp = 100), 'PLAYER', 32, 64)
ourEntities = entities()
ourEntities.addEntity(npcPiece("baddie.png", 3, [320,200], 2, 1, PStats(hp = 100), 'BADDIE', 32, 64, ai_state = "chase_player"))
ourEntities.addEntity(npcPiece("baddie.png", 3, [360,260], 2, 1, PStats(hp = 100), 'BADDIE2', 32, 64, ai_state = "chase_player"))
ourEntities.addEntity(npcPiece("eilf2b.png", 3, [360,320], 2, 1, PStats(hp = 100), 'BADDIE3', 32, 64, ai_state = "chase_player"))
ourEntities.addEntity(npcPiece("baddie.png", 3, [352,200], 2, 1, PStats(hp = 100), 'BADDIE4', 32, 64, ai_state = "chase_player"))
ourEntities.addEntity(npcPiece("baddie.png", 3, [352,232], 2, 1, PStats(hp = 100), 'BADDIE5', 32, 64, ai_state = "chase_player"))

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
action_meter = meter(0, 300, 300, 1, True)
geom_system = geom_draw_system()
# code for testing animated line geometry
#testLine = animated_line([(480, 32), (480, 32), (480, 32), (480, 32)], [(360, 64), (400, 98), (440, 128), (480, 164)], (255, 0, 0), 2, 10, anim_looping = True)

for k in range(ourScript.header[0]):
	if k != 0:
		currTile = Surface((32, 32)).convert()
		currTile.fill((0, 255, 255))
		currTile.set_alpha(75)
		gui.draw_text_block(1, 1, currTile, str(k+1))
		print ourScript.defs[k][1]
		scriptTiles.append(currTile)

test_astar_path = None

while 1:
	clock.tick(60) #keep the framerate at 60 or lower
	timeTicks = pygame.time.get_ticks()
	geom_system.update() # update geom systemtest_astar_path
	#print clock.get_fps()	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if (event.type == pygame.MOUSEMOTION) & (geom_system.is_mode_enabled() == True):
			geom_system.update_mode_mouse_position(pygame.mouse.get_pos())
		if (event.type == pygame.MOUSEBUTTONDOWN) & (geom_system.is_mode_enabled() == True):
			geom_system.press_mouse_click()
			
	key=pygame.key.get_pressed()
	if key[pygame.K_q]: 
		sys.exit()

	if (key[pygame.K_LCTRL]) & (geom_system.is_mode_button_pressed() == False):
		geom_system.press_mode_button(ourPiece.pos[0] + 16 - offs_x, ourPiece.pos[1] + 32 - offs_y, action_meter.get_value())
		geom_system.update_mode_mouse_position(pygame.mouse.get_pos())

	if (key[pygame.K_LALT]) & (geom_system.is_mode_enabled() == True):
		geom_system.__init__()

	if geom_system.is_mode_enabled() == False:
		# replenish action meter as long as geom mode isn't happening
		action_meter.update()
		if geom_system.hits_calculated == False:
			if len(ourEntities._list) > 0:
				for piece in ourEntities._list:
					if (geom_system.does_collide(piece.fullrect) == True):
						piece.explode()
						#piece.exploding = True
			geom_system.hits_calculated = True
			action_meter.set_value(action_meter.get_value() - geom_system.calculate_distanced_used())

		if key[pygame.K_n] & ourPiece.exploded == True:
			ourPiece.clear_death(hp = 100)
			ourPiece.pos[0] = 480
			ourPiece.pos[1] = 32
			ourPiece.update(direction = 0, redrawOnly = True)
		
		if key[pygame.K_TAB]:
			if(showDetails == True):
				showDetails = False
			else:
				showDetails = True

		if key[pygame.K_z]:
			if(showScriptTiles == True):
				action_meter.start_updating()
				showScriptTiles = False
			else:
				action_meter.stop_updating()
				showScriptTiles = True

		if ourPiece.exploding == False:
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

	if test_astar_path == None:
		# just testing pathfinding with A*
		ourEntities._list[0].calculate_astar_path((22, 9), astar.script_to_grid(ourScript))
		test_astar_path = ourEntities._list[0].current_astar_path
		for i in range(len(test_astar_path)):
			usethis_x = offs_x
			usethis_y = offs_y
			if (offs_x < 0): 
				usethis_x = 0
			if (offs_y < 0):
				usethis_y = 0
			test_astar_path[i] = (test_astar_path[i][0] * 32 - usethis_x + 16, test_astar_path[i][1] * 32 - usethis_y + 16)

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
		# remove any blown up from the list
		if otherEntities.exploded == True:
			ourEntities.removeEntity(ID = otherEntities.id)
		otherEntities.moving = True

		# choose facing for piece animation, as well as movement direction
		otherEntities.choose_facing(ourPiece.pos)				print "BARGAGGLE"
		# update piece to move towards movement direction
		otherEntities.update(otherEntities.get_movement_direction())
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
		screen = gui.draw_text_block(15, 78, screen, "Action Meter: " + str(action_meter.get_value()))

# code for testing animated line geometry
	#testLine.update([offs_x, offs_y])
	#testLine.draw(screen)
	if geom_system.is_mode_enabled() == True:
		geom_system.draw_system(screen, (255, 0, 0))

	pygame.draw.lines(screen, (0, 0, 255), False, test_astar_path, 2)
	action_meter.render_bar(screen)
	
	pygame.display.update()
