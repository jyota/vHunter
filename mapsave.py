import csv
import array

def savemap(filename, mapheader, mapdata):
	'''Load a map with header name, tileset name, script name, width, height, layers  delimited by commas, 
	then each data piece delimited by commas.'''

	#the map header

	with open(filename, 'w') as f:
		map_writer = csv.writer(f, delimiter=',')
		map_writer.writerow(mapheader)
		for i in range(0, mapheader[5]):
			for j in range(0, mapheader[4]):
				map_writer.writerow(mapdata[i][j][:])

	return
