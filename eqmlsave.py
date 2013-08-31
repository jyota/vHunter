import csv
import array

def saveeqml(filename, eqmldata):
	'''Save equipment list data to a file.'''

	with open(filename, 'w') as f:
		script_writer = csv.writer(f, delimiter=',')
		for i in range(0, len(eqmldata)):
			script_writer.writerow(eqmldata[i][:])

	return
