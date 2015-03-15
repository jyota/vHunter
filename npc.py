import piece
import astar
import random
import pygame
from pygame import Rect
from geom_intersection import *
# handles non-player controlled pieces, mainly because they'll require control outside of player's hands
# and I don't want to add that to the Piece class since it is also used for the player.

npc_ai_states_allowed = ("stationary", "chase_player", "chase_objective_location", "attacking") # list of possible AI states

class npcPiece(piece.Piece):
	def __init__(self, filename, framesperdir, initpos = [0,0],  initdir = None, speed = None, stats = None, id = None, width = 32, height = 64, ai_state = None, attack_image_filename = None, current_goal = (22, 9)):
		if any(ai_state in i for i in npc_ai_states_allowed):
			self.ai_state = ai_state
		else:
			raise Exception("npcPiece ai_state not in npc_ai_states_allowed!")

		self.current_astar_path = None  # hold A* path if one found
		self.next_astar_node = None
		self.movement_direction = None
		self.grid_rects = None
		self.only_stationary = False
		self.previous_ai_state = None
		self.current_goal = current_goal
		self.attack_initialized = False
		self._attack_images = []
		self.dont_play_around_increment = 0 # if piece switches to "chase player" 6 times, I want the piece to then only chase the goal.
		self.does_chase_player = (random.randint(0, 10) > 5) # randomly determine if piece should chase player while in range
		super(npcPiece, self).__init__(filename, framesperdir, initpos, initdir, speed, stats, id, width, height)
		if attack_image_filename != None:
			image = pygame.image.load(attack_image_filename).convert()

			for j in range(0, (image.get_height()/64)):
				for i in range(0, (image.get_width()/32)):
					self._attack_images.append(image.subsurface(Rect((i*32, j*32, 32, 64))).convert())
					self._attack_images[len(self._attack_images) - 1].set_colorkey((0, 0, 0))
		

	def set_ai_state(self, state):
		if any(state in i for i in npc_ai_states_allowed):
			self.ai_state = state
			return True
		else:
			return False

	def get_ai_state(self):
		return self.ai_state

	def toggle_only_stationary(self):
		if self.only_stationary == False:
			self.only_stationary = True
		else:
			self.only_stationary = False

	def get_movement_direction(self):
		return self.movement_direction

	def attack_data_shift(self, direction):
		if self.attack_initialized == False and self.ai_state == "attacking":
			oldImages = self._images 
			self._images = self._attack_images
			self._attack_images = oldImages	
			self.movement_direction = None
			self.animoffset = direction	
			self._delay = 125
			self.attack_initialized = True
		elif self.ai_state != "attacking":
			self.attack_initialized = False
			oldImages = self._images 
			self._images = self._attack_images
			self._attack_images = oldImages
			self._delay = 250
		elif self.ai_state == "attacking":
			self.animoffset = direction

	def should_attack_shift(self, player_pos = None, goal_piece_pos = None):
		if self.ai_state != "attacking":
			self.previous_ai_state = self.ai_state

		if player_pos != None:
			if ((self.pos[0] + 16) >= (player_pos[0] - 10)) and ((self.pos[0] + 16) <= (player_pos[0] + 40)) and ((self.pos[1] + 36) <= (player_pos[1] + 64)) and ((self.pos[1] + 36) > (player_pos[1] + 32)):
				self.ai_state = "attacking"
				self.attack_data_shift(0)
			elif ((self.pos[0] + 16) >= (player_pos[0] - 10)) and ((self.pos[0] + 16) <= (player_pos[0] + 40)) and ((self.pos[1] + 62) >= (player_pos[1] + 32)) and ((self.pos[1] + 64) < (player_pos[1] + 64)):
				self.ai_state = "attacking"
				self.attack_data_shift(2)
			elif ((self.pos[0] - 2) <= (player_pos[0] + 26)) and (self.pos[0] > (player_pos[0] + 26)) and ((self.pos[1] + 32) >= (player_pos[1] + 6)) and ((self.pos[1] + 32) < (player_pos[1] + 58)):
				self.ai_state = "attacking"
				self.attack_data_shift(1)			
			elif ((self.pos[0] + 28) >= player_pos[0]) and (self.pos[0] < player_pos[0]) and ((self.pos[1] + 32) >= (player_pos[1] + 6)) and ((self.pos[1] + 32) < (player_pos[1] + 58)):
				self.ai_state = "attacking"
				self.attack_data_shift(3)
			elif self.ai_state == "attacking":
				self.ai_state = self.previous_ai_state
				self.attack_data_shift(None)

	def check_goal_state_shift(self, player_pos, grid, entity_list, threshold = 200):
		# function will be used to determine whether to shift NPC state to one of the available states. 
		# highly un-optimized right now...
		if (self.only_stationary == True):
			self.ai_state = "stationary"
		elif self.ai_state == "attacking":
			self.should_attack_shift(player_pos = player_pos, goal_piece_pos = (25, 25)) # need to change goal piece pos, just filler for now
		elif (self.does_chase_player == True) and (self.ai_state == "chase_objective_location"):
			if ((abs((self.pos[0] + 16) - (player_pos[0] + 16)) < 96) and (abs((self.pos[1] + 32) - (player_pos[1] + 32)) < 96)):
				if self.grid_rects == None:
					self.grid_rects = []
					for y in range(len(grid)):
						for x in range(len(grid[0])):
							if grid[x][y] == False:
								self.grid_rects.append(Rect((x * 32, y * 32), (32, 32)))

				shiftState = True

				for z in self.grid_rects:
					res = calculateLineIntersectsRectangle((self.pos[0] + 16, self.pos[1] + 8), (player_pos[0] + 16, player_pos[1] + 58), z)
					res2 = calculateLineIntersectsRectangle((self.pos[0] + 2, self.pos[1] + 8), (player_pos[0] + 16, player_pos[1] + 58), z)
					res3 = calculateLineIntersectsRectangle((self.pos[0] + 31, self.pos[1] + 8), (player_pos[0] + 16, player_pos[1] + 58), z)
					res4 = calculateLineIntersectsRectangle((self.pos[0] + 16, self.pos[1] + 64), (player_pos[0] + 16, player_pos[1] + 58), z)
					res5 = calculateLineIntersectsRectangle((self.pos[0] + 2, self.pos[1] + 64), (player_pos[0] + 16, player_pos[1] + 58), z)
					res6 = calculateLineIntersectsRectangle((self.pos[0] + 31, self.pos[1] + 64), (player_pos[0] + 16, player_pos[1] + 58), z)					
					if ((len(res) > 0) or (len(res2) > 0) or (len(res3) > 0) or (len(res4) > 0) or (len(res5) > 0) or (len(res6) > 0)):
						shiftState = False 
						break

				if (shiftState == True) and (self.dont_play_around_increment < 6):
					self.previous_ai_state = self.ai_state
					self.ai_state = "chase_player"
					self.dont_play_around_increment = self.dont_play_around_increment + 1
				elif shiftState == False:
					self.should_attack_shift(goal_piece_pos = (25, 25)) # filler position! need to change
		elif (self.ai_state == "chase_player"):
			if ((abs((self.pos[0] + 16) - (player_pos[0] + 16)) < 96) and (abs((self.pos[1] + 32) - (player_pos[1] + 32)) < 96)):
				if self.grid_rects == None:
					self.grid_rects = []
					for y in range(len(grid)):
						for x in range(len(grid[0])):
							if grid[x][y] == False:
								self.grid_rects.append(Rect((x * 32, y * 32), (32, 32)))
				shiftState = False

				for z in self.grid_rects:
					res = calculateLineIntersectsRectangle((self.pos[0] + 16, self.pos[1] + 8), (player_pos[0] + 16, player_pos[1] + 58), z)
					res2 = calculateLineIntersectsRectangle((self.pos[0] + 2, self.pos[1] + 8), (player_pos[0] + 16, player_pos[1] + 58), z)
					res3 = calculateLineIntersectsRectangle((self.pos[0] + 31, self.pos[1] + 8), (player_pos[0] + 16, player_pos[1] + 58), z)
					res4 = calculateLineIntersectsRectangle((self.pos[0] + 16, self.pos[1] + 58), (player_pos[0] + 16, player_pos[1] + 58), z)
					res5 = calculateLineIntersectsRectangle((self.pos[0] + 2, self.pos[1] + 58), (player_pos[0] + 16, player_pos[1] + 58), z)
					res6 = calculateLineIntersectsRectangle((self.pos[0] + 31, self.pos[1] + 58), (player_pos[0] + 16, player_pos[1] + 58), z)					
					if ((len(res) > 0) or (len(res2) > 0) or (len(res3) > 0) or (len(res4) > 0) or (len(res5) > 0) or (len(res6) > 0)):
						shiftState = True 
						break

				if shiftState == True:
					self.previous_ai_state = self.ai_state
					self.ai_state = "chase_objective_location"
					self.calculate_astar_path(grid) 
				else:
					self.should_attack_shift(player_pos = player_pos)
			else:
				self.previous_ai_state = self.ai_state
				self.ai_state = "chase_objective_location"
				self.calculate_astar_path(grid)    


	def calculate_astar_path(self, grid):
		self.current_astar_path = astar.create_path((int(round(self.colrect.left / 32.0, 0)), int(round(self.colrect.top / 32.0, 0))), self.current_goal, grid)
		self.next_astar_node = 0

	def choose_facing(self, player_pos):
		this_state = self.get_ai_state()
		if this_state ==  "chase_objective_location":
			# A* path follow logic
			if (self.next_astar_node != None) & (self.next_astar_node != len(self.current_astar_path)):
				target_pos = self.current_astar_path[self.next_astar_node]
				t_x = target_pos[0] * 32 
				t_y = target_pos[1] * 32
				if (self.next_astar_node < len(self.current_astar_path)) and (round((self.pos[0]) / 32.0, 1) == target_pos[0]) & (round((self.pos[1] + 32) / 32.0, 1) == target_pos[1]):
					self.next_astar_node = self.next_astar_node + 1
				else:
					if ((self.current_astar_path[self.next_astar_node][0] == self.current_astar_path[self.next_astar_node - 1][0]) & ((self.pos[1] + 32) < t_y)):
						self.animoffset = 2
					elif ((self.current_astar_path[self.next_astar_node][0] == self.current_astar_path[self.next_astar_node - 1][0]) & ((self.pos[1] + 32) > t_y)):
						self.animoffset = 0
					elif (self.pos[0] < t_x):
						self.animoffset = 3
					else:
						self.animoffset = 1
				
					# now set actual movement direction
					if abs((self.pos[0]) - t_x) > abs((self.pos[1] + 32) - t_y):
						if ((self.pos[0]) > t_x):
							self.movement_direction = 1
						else:
							self.movement_direction = 3
					else:	
						if ((self.pos[1] + 32) > t_y):
							self.movement_direction = 0
						else:
							self.movement_direction = 2
			else:
				self.movement_direction = None
				self.ai_state = "stationary"
		elif (this_state == "chase_player"):
			# basic player chasing logic
			# first change animation offset only
			# need to make the animation offsetting a little better
			if (self.pos[0] > (player_pos[0] - 32)) & (self.pos[0] < (player_pos[0] + 32)) & (self.pos[1] < player_pos[1]):
				self.animoffset = 2
			elif (self.pos[0] > (player_pos[0] - 32)) & (self.pos[0] < (player_pos[0] + 32)) & (self.pos[1] > player_pos[1]):
				self.animoffset = 0
			elif (self.pos[0] < player_pos[0]):
				self.animoffset = 3
			else:
				self.animoffset = 1
			
			# now set actual movement direction
			if abs(self.pos[0] - player_pos[0]) > abs(self.pos[1] - player_pos[1]):
				if (self.pos[0] >= player_pos[0]):
					self.movement_direction = 1
				else:
					self.movement_direction = 3
			else:
				if (self.pos[1] >= player_pos[1]):
					self.movement_direction = 0
				else:
					self.movement_direction = 2

	
