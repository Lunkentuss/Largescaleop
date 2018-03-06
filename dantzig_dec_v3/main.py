import matplotlib.pyplot as plt 
from dantzig import dantzig
from amplpy import AMPL

def main():
	model_path = 'mod.mod'
	data_path = 'dat.dat'
	#data_path = '../data/dat11.dat'

	ampl = AMPL()
	ampl.read(model_path)
	ampl.readData(data_path)

	# tuple(0) := solutions, tuple(1) := ) 
	tuple_dantzig = dantzig(ampl,data_path)
	# TIME:x Upperbound:y
	plt.plot(tuple_dantzig[2],tuple_dantzig[1])

	# Iteration:x Upperbound:y
	#plt.plot([x+1 for x in range(len(tuple_dantzig[1]))],tuple_dantzig[1])

	plt.show(block=False)
	plt.show()

if __name__ == '__main__':
	main()
