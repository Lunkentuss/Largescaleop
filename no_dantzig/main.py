from amplpy import AMPL

ampl = AMPL()

ampl.read('mod.mod')
ampl.readData('dat.dat')
ampl.setOption('solver','cplex')

ampl.solve()
