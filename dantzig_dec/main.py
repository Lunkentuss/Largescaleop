import sys
sys.path.append('../utils/')
from amplpy import AMPL, DataFrame
from getpara import *

ampl = AMPL()

ampl.read('mod.mod')
ampl.readData('dat.dat')
ampl.setOption('solver','cplex')

# Get nbr of machines and the set 
mach_list = set2list(ampl,'K_mach_RESOURCES')
nbr_of_machines = len(mach_list)
#print('Number of machines: ' + repr(nbr_of_machines))
#print('Machines: ' + repr(mach_list))

## Get the nbr of max jobs
nbr_of_jobs = getSingleParameter(ampl,'maxjobs')
nbr_of_jobs = int(nbr_of_jobs)
#print('Number of jobs: ' + repr(nbr_of_jobs))


# Set A and B
