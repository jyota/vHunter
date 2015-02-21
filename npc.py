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
		super(npcPiece, self).__init__(filename, framesperdir, initpos, initdir, speed, stats, id, width, height)

	def set_ai_state(self, state):
		if any(state in i for i in npc_ai_states_allowed):
			self.ai_state = state
			return True
		else:
			return False

	def get_ai_state(self):
		return self.ai_state

	def check_goal_state_shift(self, player_pos, grid, entity_list, threshold = 200):
		# function will be used to determine whether to shift NPC state to one of the available states. 
		# requires information about environment to make this decision, so whatever is relevant to do this will probably need to be passed in here.
		pass

	def calculate_astar_path(self, objective_location, grid):
		self.current_astar_path = astar.create_path((int(round(self.colrect.left / 32.0, 0)), int(round(self.colrect.top / 32.0, 0))), objective_location, grid)

