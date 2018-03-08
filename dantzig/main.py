import matplotlib.pyplot as plt 
from dantzig import dantzig
from amplpy import AMPL

def main():
	model_path = 'mod.mod'
	data_path = '../data/dat3.dat'

	ampl = AMPL()
	ampl.read(model_path)
	ampl.readData(data_path)

	nbr_of_jobs = int(ampl.getParameter('maxjobs').getValues().toList()[0][0])
	A = [1 for i in range(nbr_of_jobs)]
	B = [1 for i in range(nbr_of_jobs)]

	max_iterations = 1000

        # tuple(0) := solutions, tuple(1) := upperbound, tuple2() := time_iteration) 
	tuple_dantzig = dantzig(ampl,A,B,data_path,max_iterations)
	# TIME:x Upperbound:y
	plt.plot(tuple_dantzig[2],tuple_dantzig[1])

	# Iteration:x Upperbound:y
	#plt.plot([x+1 for x in range(len(tuple_dantzig[1]))],tuple_dantzig[1])

	plt.show(block=False)
	plt.show()

if __name__ == '__main__':
	main()
