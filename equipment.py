

class PEquipment():
	def __init__(self, items = []):
		self.items = items
		''' Format for items: [0] = ID, [1] = Type, [2] = Name, [3] = Modifier, [4] = special effects '''
		self.eqpWeapon = None


	def add_equipment(self, item = None):
		if item != None:
			self.items.append(item)

	def get_length(self):
		return len(self.items)

	def equip_weapon_by_id(self, id):
		''' Copy the "equipped weapon" into the eqpWeapon part of this class. '''
		for j in self.items:
			if j[0] == id:
				self.eqpWeapon = j

	def get_equipment_by_id(self, id):
		for i in self.items:
			if i[0] == id:
				return i

	def remove_equipment(self, item_id = None):
		if item_id != None:	
			allitems = []
			gotit = 0
			for i in self.items:
				if i[0] == item_id and gotit == 0:
					gotit = 1
				else:
					allitems.append(i)

		self.items = allitems
