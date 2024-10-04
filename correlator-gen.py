import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

def InitCorrelator(this):
	# make some time indices
	time_indices = np.arange(this['tap count'])
	# Now scale the time indices according to frequency.
	time_indices = time_indices * (2.0 * np.pi * this['frequency']/ this['sample rate'])
	# Calculate the waveforms.
	this['SinTaps'] = np.sin(time_indices)
	this['CosTaps'] = np.cos(time_indices)
	return this

def GenInt16ArrayC(name, array, column_width):
	result = '\n'
	result += f'const __prog__ int16_t __attribute__((space(prog))) {name}[{len(array)}] = '
	result += '{ '
	y = len(array)
	for x in range(y):
		if x % column_width == 0:
			result += ' \\\n     '
		result += f' {int(np.rint(array[x]))}'
		if x < (y-1):
			result += ','
	result += ' };'
	return result

if len(sys.argv) != 5:
		print("Not enough arguments. Usage: python3 correlator-gen.py <sample rate> <frequency> <amplitude> <tap count>")
		sys.exit(-1)

correlator = {}
correlator['sample rate'] = float(sys.argv[1])
correlator['frequency'] = float(sys.argv[2])
correlator['amplitude'] = float(sys.argv[3])
correlator['tap count'] = int(sys.argv[4])

correlator = InitCorrelator(correlator)

plt.figure()
plt.plot(correlator['SinTaps'])
plt.plot(correlator['CosTaps'])
plt.title(f'Correlator {correlator["frequency"]} Hz, {correlator["sample rate"]} samp/sec')
plt.grid()
plt.show()


#generate a new director for the reports
run_number = 0
print('trying to make a new directory')
while True:
	run_number = run_number + 1
	dirname = f'./run{run_number}/'
	try:
		os.mkdir(dirname)
	except:
		print(dirname + ' exists')
		continue
	print(f'made new directory {dirname}')
	break

# Generate and save report file
report_file_name = f'run{run_number}_report.txt'
try:
	report_file = open(dirname + report_file_name, 'w+')
except:
	print('Unable to create report file.')
with report_file:
	report_file.write('# Command line: ')
	for argument in sys.argv:
		report_file.write(f'{argument} ')

	report_file.write(f'\n\n# Correlator {correlator["frequency"]}Hz\n')
	report_file.write('\n')
	report_file.write(GenInt16ArrayC(f'Sin{int(correlator["frequency"])}_{int(correlator["sample rate"])}', correlator['SinTaps'] * correlator['amplitude'], 10))
	report_file.write(GenInt16ArrayC(f'Cos{int(correlator["frequency"])}_{int(correlator["sample rate"])}', correlator['CosTaps'] * correlator['amplitude'], 10))
	report_file.write('\n')
	report_file.close()
	print(f'wrote {dirname + report_file_name}')
