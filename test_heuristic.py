from amplpy import AMPL
from typing import NewType

# Create AMPL instance
ampl = AMPL()

ampl.read('model_template.mod')
#ampl.readData('test_heuristic.dat')
ampl.setOption('solver','cplex')

# Get sets and parameters from ampl model
#JOBS = ampl.getSet('JOBS')
K_mach_RESOURCES = ampl.getSet('K_mach_RESOURCES')
JOBS = ampl.getSet('JOBS')
maxjobs = ampl.getParameter('maxjobs')#.getValues()
a_disc = ampl.getParameter('a_disc')
r_disc = ampl.getParameter('r_disc')
proc_time_disc = ampl.getParameter('proc_time_disc')
p_j_o_postmach_disc = ampl.getParameter('p_j_o_postmach_disc')
lambda_mach = ampl.getParameter('lambda_mach')

# Set Parameters to integers
maxjobs = NewType('maxjobs', int)
lambda_mach = NewType('lambda_mach', int)

# Set test values
maxjobs = 10
JOBS_left = list(range(1,maxjobs+1)) # name jobs 1,...,maxjobs
lambda_mach = [[1 for col in range(5)] for row in range(maxjobs)] # set elements in lambda to 0 or 1
lambda_mach[0][0] = 0
lambda_mach[0][4] = 0
lambda_mach[1][1] = 0
lambda_mach[2][1] = 0
lambda_mach[6][3] = 0
lambda_mach[9][0] = 0



# Heuristic
while (len(JOBS_left) > 0):
    JOBS_left.pop(0)
    print(JOBS_left)

