class BFSNode:
	def __init__(self, x, y, cost, parent=None):
		self.x = x
		self.y = y
		self.cost = cost
		self.parent = parent

	def __eq__(self, l):
		if l.x == self.x and l.y == self.y:
			return 1
		else:
			return 0

class BFS:
	def __init__(self, startx, starty, mp, map):
		self.startx = startx
		self.starty = starty
		self.mp = mp
		self.mapData = map.data
		self.mW = map.header[1]
		self.mH = map.header[2]

	def findPath(self):
		worknodes = list()
		opennodes = list()

		startNode = BFSNode(self.startx, self.starty, 0)

		worknodes.insert(0, BFSNode(self.startx+1,self.starty, 1, startNode))
		worknodes.insert(0, BFSNode(self.startx-1,self.starty, 1, startNode))
		worknodes.insert(0, BFSNode(self.startx,self.starty+1, 1, startNode))
		worknodes.insert(0, BFSNode(self.startx,self.starty-1, 1, startNode))

		for i in worknodes:
			if i.x > -1 and i.y > -1 and i.x < self.mW and i.y < self.mH and self.mapData[i.y][i.x] != 1:
				opennodes.insert(0, i)

		for j in range(1, self.mp):
			worknodes = list()

			for i in opennodes:
				worknodes.insert(0, BFSNode(i.x+1, i.y, j, i))
				worknodes.insert(0, BFSNode(i.x-1, i.y, j, i))
				worknodes.insert(0, BFSNode(i.x, i.y+1, j, i))
				worknodes.insert(0, BFSNode(i.x, i.y-1, j, i))

			for i in worknodes:
				if i.x > -1 and i.y > -1 and i.x < self.mW and i.y < self.mH and self.mapData[i.y][i.x] != 1:
					opennodes.insert(0, i)

		returnList = list()
		for i in opennodes:
			if i not in returnList:
				returnList.append(i)

		returner = list()
		for i in returnList:
			choice = [i.x, i.y]
			returner.append(choice)

		return returner
