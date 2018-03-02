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

# Set A[j] and B[j]


# Find feasible solution from heuristic and set x[1,k,j]
# in ampl


# Calculate RMP for the feasible solution(objective value)


# Loop for column generation


max_iterations = 1000;
l = 2;
while(1):
	# Solve dual RMP

	# Solve column generation problem and update x_bar

	# Solve RMP (pessimistic bound)

	# Optimistic bound??????

	# Termination criteria == 1 (close enough criteria)
	if(1 != 1 or l >= max_iterations): 
		break;

	l = l + 1;

# Solve RMP with binary constraint
