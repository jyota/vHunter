

class PStats():
	def __init__(self, hp = 0, ep = 0, attack = 0, eattack = 0, defense = 0, edefense = 0, tough = 0, level = 0, XP = 0, AP = 0):
		self.hp = hp
		self.ep = ep
		self.attack = attack
		self.eattack = eattack
		self.defense = defense
		self.edefense = edefense
		self.tough = tough
		self.level = level
		self.XP = XP
		self.AP = AP
		self.status = 0 
		''' Always start status as 0. This will be filled later as needed will values'''
		''' that represent things like poison, speed up, or whatever. '''


	
