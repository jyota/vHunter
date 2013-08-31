import eqmlload
from eqmlload import *
import eqmlsave
from eqmlsave import *

class EQML():
	def __init__(self, filename=None):
		''' Equipment master list for game. '''
		if filename != None:
			self.eqpMaster = loadeqml(filename)

	def get_equipment_by_id(self, id):
		if id != None:
			for i in self.eqpMaster:
				if i[0] == id:
					return i

	def add_item(self, item = None):
		if item != None:
			self.eqpMaster.append(item)

	def remove_item(self, item_id = None):
		if item_id != None:
			allitems = []
			gotit = 0
			for i in self.eqpMaster:
				if i[0] == item_id and gotit == 0:
					gotit = 1
				else:
					allitems.append(i)

			self.eqpMaster = allitems
	
	def get_length(self):
		return len(self.eqpMaster)

	def save_item_list(self, filename=None):
		if filename != None:
			saveeqml(filename, self.eqpMaster)
