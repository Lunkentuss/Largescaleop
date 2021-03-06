import sys
sys.path.append("../../utils/")

from amplpy import AMPL
from getpara import * 

ampl = AMPL()

ampl.read('model.mod')
ampl.readData('dat.dat')
ampl.setOption('solver','cplex')

flexdf = ampl.getParameter('lambda_mach').getValues()

maxjobs = getSingleParameter(ampl,'maxjobs')

flexmat = flexdf2mat(flexdf,int(maxjobs),5)

#print(flexmat)

a_disc_list = ampl.getParameter('a_disc').getValues().toList()

l = [a_disc_list[k][1] for k in range(5)]
print(l)
