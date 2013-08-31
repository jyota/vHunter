import csv
import array

def loadeqml(filename):
	'''Load equipment list delimited by commas. Can't have any empty lines. '''
	eqml = []
	first = True

	with open(filename, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			eqml.append(row)		

	
	for i in range(0, len(eqml)):
		for j in range(0, 4):
			if j == 0:
				eqml[i][j] = int(eqml[i][j])
			elif j == 3:
				eqml[i][j] = int(eqml[i][j])

	return eqml

