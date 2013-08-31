import csv
import array

def loadmap(filename):
	'''Load a map with header name, tileset name, script name, width, height, layers  delimited by commas, 
	then each data piece delimited by commas.'''

	#the map header
	mapheader = []

	j = 0
	layer = 0

	firstrow = True

	with open(filename, 'r') as f:
		reader = csv.reader(f)
		for row in reader:

			if firstrow == True:
				mapheader.append(row[0])           
				mapheader.append(row[1])           
				mapheader.append(row[2])      
				mapheader.append(int(row[3]))      
				mapheader.append(int(row[4]))      
				mapheader.append(int(row[5]))      
				firstrow = False
				mapdata = [[ [ 0 for k in range(mapheader[3])] for l in range(mapheader[4])] for m in range(mapheader[5])]
			else:
				i = 0
				 
				for i in range(0,len(row)):
					mapdata[layer][j][i] = int(row[i])

				if j == (mapheader[4] - 1):
					layer += 1 
					j = 0
				else: 
					j += 1


	return mapheader, mapdata;

