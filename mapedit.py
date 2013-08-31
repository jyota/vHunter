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

def tile_brush_chooser(wheretodraw, mapfortiles):
	''' Select a tile from a World object's tileset using the mouse and return it's index for reference. '''
	maxx = 0
	maxy = 0
	thisx = 0
	thisy = 0

	while 1:
		wheretodraw.fill((0, 0, 0, 0))
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				whichx, whichy = pygame.mouse.get_pos()
				whichx = (whichx / 32)
				whichy = (whichy / 32)
				if (whichy > (maxy * 32)) and (whichx > (maxx * 32)):
					return 0
				else:
					if whichy == 0:
						return whichx
					else:
						return ((whichy * 20) + whichx)
	
		for tile in mapfortiles.tileset:
			wheretodraw.blit(tile, (thisx * 32, thisy * 32))
			if ((thisx * 32) > 607):
				maxx = thisx
				thisx = 0
				thisy = thisy + 1
			else: 
				thisx = thisx + 1

		maxy = thisy
		thisx = 0
		thisy = 0
		
		tmx, tmy = pygame.mouse.get_pos()
		if (tmx > 0) and (tmy > 0):
			pygame.draw.rect(wheretodraw, (255, 255, 255), ((tmx / 32) * 32, (tmy / 32) * 32, 32, 32), 1)
		pygame.display.flip()


pygame.init()
pygame.font.init()

tileselected = 0

screen = pygame.display.set_mode((640, 480))
pygame.display.update()
pygame.mouse.set_visible(True)
mapselect = create_text_input(screen, "Enter filename (for map):")
mapselect.value = "default.map"
scrselect = create_text_input(screen, "Enter filename (for script):")
scrselect.value = "default.scr"

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
offs_x, offs_y = (0, 0)
currentScript = 0
scriptTiles = []

collTile = Surface((32, 32))
collTile.fill((255, 0, 0))
collTile.set_alpha(68)

scriptTiles.append(collTile)

for k in range(ourScript.header[0]):
	if k != 0:
		currTile = Surface((32, 32))
		currTile.fill((0, 255, 255))
		currTile.set_alpha(75)
		gui.draw_text_block(1, 1, currTile, str(k+1))
		print ourScript.defs[k][1]
		scriptTiles.append(currTile)

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				# select a filename to save this map to
				get_text_kb(mapselect, screen)
			if event.key == pygame.K_s:
				# save the current map and script in memory
				ourMap.header[2] = scrselect.value
				savemap(mapselect.value, ourMap.header, ourMap.data)
				savescript(scrselect.value, ourScript.header, ourScript.defs, ourScript.data)
			if event.key == pygame.K_q: 
				sys.exit()
			if event.key == pygame.K_F1:
				get_text_kb(scrselect, screen)
			if event.key == pygame.K_F2:
				# call the tile selection subroutine.
				tileselected = tile_brush_chooser(screen, ourMap)
			if event.key == pygame.K_0:
				currentLayer = 0
			if event.key == pygame.K_1:
				if(ourMap.header[5]==2):
					currentLayer = 1
			if event.key == pygame.K_2:
				if(ourMap.header[5]==3):
					currentLayer = 2
			if event.key == pygame.K_3:
				if(ourMap.header[5]==4):
					currentLayer = 3
			if event.key == pygame.K_4:
				if(ourMap.header[5]==5):
					currentLayer = 4
			if event.key == pygame.K_d:
				ourMap.data[currentLayer][((offs_y + tmy)/32)][((offs_x + tmx)/32)] = 0
			if event.key == pygame.K_z:
				ourScript.data[((offs_y + tmy)/32)][((offs_x + tmx)/32)] = currentScript
			if event.key == pygame.K_x:
				ourScript.data[((offs_y + tmy)/32)][((offs_x + tmx)/32)] = 0
			if event.key == pygame.K_PERIOD:
				currentScript = currentScript + 1
				if (currentScript == ourScript.header[0]):
					currentScript = currentScript - 1
			if event.key == pygame.K_COMMA:
				currentScript = currentScript - 1
				if (currentScript < 0):
					currentScript = 0
			if event.key == pygame.K_TAB:
				if(showDetails == True):
					showDetails = False
				else:
					showDetails = True

		if event.type == pygame.MOUSEBUTTONDOWN:
			ourMap.data[currentLayer][((offs_y + tmy)/32)][((offs_x + tmx)/32)] = tileselected

	#Scrolling map logic
	tmx, tmy = pygame.mouse.get_pos()
	if((tmx<20) and (offs_x > 0)): offs_x -= 2
	if((tmx>620) and (offs_x < ourMap.header[3]*32)): offs_x += 2
	if((tmy<20) and (offs_y > 0)): offs_y  -= 2
	if((tmy>460) and (offs_y < ourMap.header[4]*32)): offs_y += 2
	if(offs_x < 0): offs_x = 0
	if(offs_y < 0): offs_y = 0
	if(offs_x > (ourMap.header[3]*32 - 640)): offs_x = ourMap.header[3]*32 - 640
	if(offs_y > (ourMap.header[4]*32 - 480)): offs_y = ourMap.header[4]*32 - 480
	
	screen.fill((0,0,0,0))
	maprender.draw_map(screen,ourMap,offs_x, offs_y)
	if(showDetails == True):
		render_script_tiles(screen, ourScript, offs_x, offs_y, scriptTiles)
		screen = gui.draw_text_block(15, 15, screen, "Current Layer: " + str(currentLayer))
		screen = gui.draw_text_block(15, 28, screen, "Current Script Item: " + str(ourScript.defs[currentScript][:]))
	
	pygame.display.flip()
