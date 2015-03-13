import piece
import astar
import random
from pygame import Rect
from geom_intersection import *
# handles non-player controlled pieces, mainly because they'll require control outside of player's hands
# and I don't want to add that to the Piece class since it is also used for the player.

npc_ai_states_allowed = ("stationary", "chase_player", "chase_objective_location", "attacking") # list of possible AI states

class npcPiece(piece.Piece):
	def __init__(self, filename, framesperdir, initpos = [0,0],  initdir = None, speed = None, stats = None, id = None, width = 32, height = 64, ai_state = None):
		if any(ai_state in i for i in npc_ai_states_allowed):
			self.ai_state = ai_state
		else:
			raise Exception("npcPiece ai_state not in npc_ai_states_allowed!")

		self.current_astar_path = None  # hold A* path if one found
		self.next_astar_node = None
		self.movement_direction = None
		self.grid_rects = None
		self.only_stationary = False
		self.dont_play_around_increment = 0 # if piece switches to "chase player" 6 times, I want the piece to then only chase the goal.
		self.does_chase_player = (random.randint(0, 10) > 5) # randomly determine if piece should chase player while in range
		super(npcPiece, self).__init__(filename, framesperdir, initpos, initdir, speed, stats, id, width, height)

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

	def check_goal_state_shift(self, player_pos, grid, entity_list, threshold = 200):
		# function will be used to determine whether to shift NPC state to one of the available states. 
		# highly un-optimized right now...
		if self.only_stationary == True:
			self.ai_state = "stationary"
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
					self.ai_state = "chase_player"
					self.dont_play_around_increment = self.dont_play_around_increment + 1
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
					self.ai_state = "chase_objective_location"
					self.calculate_astar_path((22, 9), grid)    
			else:
				self.ai_state = "chase_objective_location"
				# NEEDS ACTUAL LEGIT objective_location, JUST A FILLER
				# Note, the piece will move to its previously calculated path without this next line, which isn't optimal from present location necessarily
				# (it may have chased player a ways off the original path)
				self.calculate_astar_path((22, 9), grid)    


	def calculate_astar_path(self, objective_location, grid):
		self.current_astar_path = astar.create_path((int(round(self.colrect.left / 32.0, 0)), int(round(self.colrect.top / 32.0, 0))), objective_location, grid)
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
		elif this_state == "chase_player":
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
		elif this_state == "stationary":
			pass

