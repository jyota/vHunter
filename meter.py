import pygame

class meter():
	def __init__(self, minimum_value, maximum_value, init_value, update_speed, updating = False, x = 530, y = 10, width = 100, height = 14, color = (0, 255, 0), border_color = (88, 88, 88), direction_multiplier = 1, speed_multiplier = 4):
		self.minimum_value = minimum_value
		self.maximum_value = maximum_value
		self.current_value = init_value
		self.update_speed = update_speed
		self.update_ticker = 0
		self.updating = updating
		# line to allow for negative 'replenish' direction later if we need
		self.direction_multiplier = direction_multiplier
		# line to allow speedup of replenish easily
		self.speed_multiplier = speed_multiplier
		self.color = color
		self.border_color = border_color
		self.meter_rect = pygame.Rect(x, y, width, height)

	def update_pos(self, x, y):
		self.meter_rect.top = y
		self.meter_rect.left = x

	def start_updating(self):
		self.updating = True

	def stop_updating(self):
		self.updating = False

	def update(self):
		if (self.updating == True) & (self.current_value < self.maximum_value) & (self.current_value >= self.minimum_value):
			if (self.update_speed > 0) & (self.update_ticker < self.update_speed):
				self.update_ticker = self.update_ticker + 1
			elif (self.update_speed > 0) & (self.update_ticker >= self.update_speed):
				self.current_value = self.current_value + (self.direction_multiplier * self.speed_multiplier)
				self.update_ticker = 0
				if (self.current_value > self.maximum_value):
					self.current_value = self.maximum_value
				if self.current_value < self.minimum_value:
					self.current_value = self.minimum_value			
		
	def get_value(self):
		return self.current_value

	def set_value(self, new_value):
		self.current_value = new_value
		# don't allow value below minimum or above maximum
		if self.current_value > self.maximum_value:
			self.current_value = self.maximum_value
		if self.current_value < self.minimum_value:
			self.current_value = self.minimum_value

	def add(self, amount):
		self.current_value = self.current_value + amount

	def sub(self, amount):
		self.current_value = self.current_value - amount

	def set_draw_location(self, draw_location):
		self.draw_location[0] = draw_location
	
	def get_draw_location(self):
		return self.draw_location[0]

	def render_bar(self, surface):
		proportion_val = float(self.current_value) / float(self.maximum_value)
		drawing_range  = round((self.meter_rect.width - 2) * proportion_val, 0)
		if drawing_range > self.meter_rect.width - 2:
			drawing_range = self.meter_rect.width - 2
		fill_rect      = pygame.Rect(self.meter_rect.left + 1, self.meter_rect.top + 1, drawing_range, self.meter_rect.height - 2)
		pygame.draw.rect(surface, self.border_color, self.meter_rect, 0)
		pygame.draw.rect(surface, self.color, fill_rect, 0)

