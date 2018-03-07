from amplpy import AMPL

ampl = AMPL()

ampl.read('mod.mod')
ampl.readData('../data/dat3.dat')
ampl.setOption('solver','cplex')

ampl.solve()
ampl.eval('display Finish_times_and_tardiness;')
