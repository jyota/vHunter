# framework for geometry drawing system (right now will just be lines with waypoints)
# i think main engine.py loop will catch the mouse clicks & positions but these will interface with the geom_draw_system to set up the line/geometry drawing & waypoints

class geom_draw_system():
	def __init__(self):
		# mode variables are related to setting mode and helper stuff for making the button not toggle the mode too quickly if button is held down briefly
		self.mode_button_counter = 0
		self.mode_button_speed = 30 
		self.mode_button_pressed = False
		self.mode_enabled = False

	def update_mode_button(self):
		if (self.mode_button_pressed == True) & (self.mode_button_counter < self.mode_button_speed):
			self.mode_button_counter = self.mode_button_counter + 1
		else:
			self.mode_button_counter = 0
			self.mode_button_pressed = False

	def is_mode_button_pressed(self):
		return self.mode_button_pressed

	def press_mode_button(self):
		self.mode_button_pressed = True
		if(self.mode_enabled == False):
			self.mode_enabled = True
		else:
			self.mode_enabled = False

	def is_mode_enabled(self):
		return self.mode_enabled


