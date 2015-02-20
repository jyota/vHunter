# A* pathfinding
import time
import pygame
import script

class node(object):
    #a very simple class simply used to store information
    def __init__(self, x, y, parent, gscore, fscore):
        self.x, self.y = x,y # position on the grid
        self.parent = parent # pointer to a parent node
        self.gscore = gscore # gscore (movement cost)
        self.fscore = fscore # h score(estimated cost)
        self.closed = False  # on closed list? y/n

def getdircost(loc1, loc2, diag_score = 16):    
    if (loc1[0] != loc2[0]) & (loc1[1] != loc2[1]):
        return diag_score # diagonal movement
    else:
        return 10 # horizontal/vertical movement

def get_h_score(start, end):
    """Gets the estimated length of the path from a node
    using the Manhattan Method."""
    #uses a heuristic function
    #return 0 #used if you want Djikstras algorithm
    return (abs(end[0]-start[0])+abs(end[1]-start[1])) * 10

def create_path(s, end, grid):
    "Creates the shortest path between s (start) and end."

    # the ons list is a 2d list of node status
    # None means the node has not been checked yet
    # a node object for a value means it is on the open list
    # a False value means that it is on the closed list
    ons = [[None for y in xrange(len(grid[x]))] for x in xrange(len(grid))]

    #n is the current best node on the open list, starting with the initial node
    n = node(s[0], s[1], None, 0, 0)

    openl = []
    
    geth = get_h_score
    while (n.x, n.y) != end:

        #search adjacent nodes
        #if the node is already on the open list, then
        #and change their pointer the the current node
        #if their path from current node is shorter than their
        #previous path from previous parent
        #if the node is not on the open list and is not a wall,
        #add it to the open list

	# heavily penalize diagonals if not in an 'open field' so pieces don't get caught on corners with diagonal movement
	# side effect of this implementation now is pieces tend to avoid walls (seems fine to me)
	diag_ok = True
        for x in xrange(n.x - 1, n.x + 2):
            for y in xrange(n.y - 1 , n.y + 2):
		if grid[x][y] == False:
			diag_ok = False

        for x in xrange(n.x - 1, n.x + 2):
            for y in xrange(n.y - 1 , n.y + 2):
                #the checked node can't be our central node
                if (x, y) != (n.x, n.y):
                    #if the node is not on the closed list or open list
                    if ons[x][y] != None:
                        if ons[x][y].closed == False:
                            #get cost of the new path made from switching parents
			    if diag_ok == False:
                            	new_cost = getdircost((n.x, n.y), (x, y), 1000) + n.gscore # diagonal not OK
			    else:
				new_cost = getdircost((n.x, n.y), (x, y)) + n.gscore # diagonal OK

                            # if the path from the current node is shorter
                            if new_cost <= ons[x][y].gscore:
                                newf = new_cost + geth((x,y), end)
                                
                                #find the index of the node
                                #to change in the open list
                                index = openl.index([ons[x][y].fscore,
                                                     ons[x][y]])

                                #update the node to include this new change
                                openl[index][1] = node(x,y, n,
                                        new_cost, newf)
                                
                                #update the ons list and the
                                #fscore list in the list
                                openl[index][0] = newf
                                ons[x][y] = openl[index][1]

                    #if the node is not a wall and not on the closed list
                    #then simply add it to the open list
                    elif grid[x][y] == True:
			    h = geth((x, y), end)

			    #movement score gets the direction cost
                            #added to the parent's directional cost
			    if diag_ok == False:
                            	g = getdircost((n.x, n.y), (x, y), 1000) + n.gscore # don't allow a diagonal
			    else:
				g = getdircost((n.x, n.y), (x, y)) + n.gscore # allow a diagonal
                            
                            ons[x][y] = node(x, y, n, g, g + h)
                            openl.append([g + h, ons[x][y]])
                            
        #if the length of the open list is zero(all nodes on closed list)
        #then return an empty path list
        if len(openl) == 0: n = None; break

        n = min(openl)
        openl.remove(n)
        n = n[1]
        
        #remove from the 'closed' list
        ons[n.x][n.y].closed = True


    #Now we have our path, we just need to trace it
    #trace the parent of every node until the beginning is reached
    moves = []
    if n!= None:
        while (n.x,n.y) != s:
            moves.insert(0,(n.x,n.y))
            n = n.parent#trace back to the previous parent
                
    return moves 

def script_to_grid(script_to_parse):
	# note since i lifted the A* grid, it reverses x and y from what I was using in my map/script matrices
	# so this flips those around for the A* grid...
	width = script_to_parse.header[1]
	height = script_to_parse.header[2]
	returning_grid = [[True for x in range(height)] for x in range(width)]
	for y in range(height):
		for x in range(width):
			if script_to_parse.defs[script_to_parse.data[y][x]][1].startswith('C') == True:
				returning_grid[x][y] = False

	return returning_grid

# some sample code for how to use this...
#myGrid = [[True for x in range(10)] for x in range(10)]
#myGrid[4][0] = False 
#yGrid[4][1] = False 
#myGrid[4][2] = False
#myGrid[4][3] = False
#myGrid[4][4] = False
#myGrid[4][5] = False
#myGrid[4][6] = False
#myGrid[4][8] = False

#res = create_path((0, 2), (5, 5), myGrid)
#print res
#print myGrid
