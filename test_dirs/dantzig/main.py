from amplpy import AMPL

import sys

sys.path.append('../../utils/')
from getpara import *

ampl = AMPL()

ampl.read('mod.mod')
#ampl.readData('dat.dat')
ampl.setOption('solver','cplex')

# Set starting values (from heuristic)
ind = ampl.getParameter('ind')
ind.setValues([1])
ampl.getParameter('row1').setValues({1:1})

# Numbers of iterations in dantzig
for i in range(2,5+1):

	print("\n")
	print("-----: " + "Iteration: " + repr(i) + " :-----")
	print("--------------------------")

	# Set solution varaibles from reduced cost problem
	ind.setValues([i])

	row1df = ampl.getParameter('row1').getValues()
	row1df.setValues({i:1})
	ampl.setData(row1df)

	#ampl.solve()
	ampl.eval('solve prob1;')

	solution = ampl.getVariable('x')
	print("Solution: " + repr(solution.getValues().toDict()))

	ampl.eval('solve prob2;')

	solution = ampl.getVariable('x')
	print("Solution: " + repr(solution.getValues().toDict()))

row1_list = para2list(ampl,'row1')
print('row1')
print(row1_list)
print(getSingleParameter(ampl,'ind',integer=False))
