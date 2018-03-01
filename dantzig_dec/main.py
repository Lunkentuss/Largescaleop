import sys
sys.path.append('../utils/')
from amplpy import AMPL, DataFrame
from getpara import *

ampl = AMPL()

ampl.read('mod.mod')
ampl.readData('dat.dat')
ampl.setOption('solver','cplex')

setSingleParameter(ampl,'maxjobs',5)
print(ampl.getParameter('maxjobs').getValues().toDict())
