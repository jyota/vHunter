
class meter():
	def __init__(self, minimum_value, maximum_value, init_value, replenish_speed, replenishing = False):
		self.minimum_value = minimum_value
		self.maximum_value = maximum_value
		self.current_value = init_value
		self.replenish_speed = replenish_speed
		self.replenish_ticker = 0
		self.replenishing = replenishing
		# line to allow for negative 'replenish' direction later if we need
		self.direction_multiplier = 1

	def start_replenishing(self):
		self.replenishing = True

	def stop_replenishing(self):
		self.replenishing = False

	def update(self):
		if (self.replenishing == True) & (self.current_value < self.maximum_value):
			if (self.replenish_speed > 0) & (self.replenish_ticker < self.replenish_speed):
				self.replenish_ticker = self.replenish_ticker + 1
			elif (self.replenish_speed > 0) & (self.replenish_ticker >= self.replenish_speed):
				self.current_value = self.current_value + self.direction_multiplier
				self.replenish_ticker = 0

	def get_current_value(self):
		return self.current_value

	def set_current_value(self, new_value):
		self.current_value = new_value


