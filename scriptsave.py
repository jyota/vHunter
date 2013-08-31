import csv
import array

def savescript(filename, scriptheader, scriptdefs, scriptdata):
	'''Save a script file. Takes filename, header, definitions, and data as arguments.'''

	with open(filename, 'w') as f:
		script_writer = csv.writer(f, delimiter=',')
		script_writer.writerow(scriptheader)
		for i in range(0, scriptheader[0]):
			script_writer.writerow(scriptdefs[i][:])

		for i in range(0, scriptheader[2]):
			script_writer.writerow(scriptdata[i][:])

	return
