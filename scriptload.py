import csv
import array

def loadscript(filename):
	'''Load a script with header and data delimited by commas. '''

	#the script header
	scriptheader = []

	j = 0
	m = 0

	firstrow = True
	dataHeader = False
	dataReading = False

	with open(filename, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			if firstrow == True:
				#Format is like: number of script data chunks, width and height 
				#(matches corresponding map), then goes into data chunks, then
				#layout based on x, y map data.
				scriptheader.append(int(row[0]))           
				scriptheader.append(int(row[1]))           
				scriptheader.append(int(row[2])) 
				scriptheader.append(row[3])
				firstrow = False
				scriptdefs = [ [ 0 for k in range(3)] for l in range(scriptheader[0])]
				scriptdata = [ [ 0 for k in range(scriptheader[1])] for l in range(scriptheader[2])]			  
				dataHeader = True

			elif dataHeader==True:
				#Read the script definitions into an array
				scriptdefs[j][0] = int(row[0])
				scriptdefs[j][1] = row[1]
				scriptdefs[j][2] = int(row[2])

				if j == scriptheader[0] - 1:
					dataHeader = False
					dataReading = True
				else:	
					j = j + 1
				
			elif dataReading == True:
				#Read the script data placed in an X, Y map

				for n in range(0, len(row)):
					scriptdata[m][n] = int(row[n])

				if m == scriptheader[2] - 1:
					m = 0
				else:
					m = m + 1
							

	return scriptheader, scriptdefs, scriptdata;

