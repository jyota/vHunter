import piece
import astar
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
		self.current_astar_dest = None
		self.movement_direction = None
		super(npcPiece, self).__init__(filename, framesperdir, initpos, initdir, speed, stats, id, width, height)

	def set_ai_state(self, state):
		if any(state in i for i in npc_ai_states_allowed):
			self.ai_state = state
			return True
		else:
			return False

	def get_ai_state(self):
		return self.ai_state

	def get_movement_direction(self):
		return self.movement_direction

	def check_goal_state_shift(self, player_pos, grid, entity_list, threshold = 200):
		# function will be used to determine whether to shift NPC state to one of the available states. 
		# requires information about environment to make this decision, so whatever is relevant to do this will probably need to be passed in here.
		pass

	def calculate_astar_path(self, objective_location, grid):
		self.current_astar_path = astar.create_path((int(round(self.colrect.left / 32.0, 0)), int(round(self.colrect.top / 32.0, 0))), objective_location, grid)
		self.current_astar_dest = self.current_astar_path[0]

	def choose_facing(self, player_pos):
		if self.get_ai_state() == "chase_player":
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

