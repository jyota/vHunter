
class meter():
	def __init__(self, minimum_value, maximum_value, init_value, update_speed, updating = False):
		self.minimum_value = minimum_value
		self.maximum_value = maximum_value
		self.current_value = init_value
		self.update_speed = update_speed
		self.update_ticker = 0
		self.updating = updating
		# line to allow for negative 'replenish' direction later if we need
		self.direction_multiplier = 1

	def start_updating(self):
		self.updating = True

	def stop_updating(self):
		self.updating = False

	def update(self):
		if (self.updating == True) & (self.current_value < self.maximum_value) & (self.current_value > self.minimum_value):
			if (self.update_speed > 0) & (self.update_ticker < self.update_speed):
				self.update_ticker = self.update_ticker + 1
			elif (self.update_speed > 0) & (self.update_ticker >= self.update_speed):
				self.current_value = self.current_value + self.direction_multiplier
				self.update_ticker = 0

	def get_value(self):
		return self.current_value

	def set_value(self, new_value):
		self.current_value = new_value

	def add(self, amount):
		self.current_value = self.current_value + amount

	def sub(self, amount):
		self.current_value = self.current_value - amount

