import sys
sys.path.append("./utils/")

from amplpy import AMPL
from typing import NewType
from getpara import *

# Create AMPL instance
ampl = AMPL()

ampl.read('model_template.mod')
ampl.readData('2010-08-16_20j_MTC6.dat')
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

# Import and convert parameters from .dat-file
maxjobs = int(getSingleParameter(ampl,'maxjobs'))
lambda_mach = flexdf2mat(ampl.getParameter('lambda_mach').getValues(),maxjobs,5)

# Initialize own parameters and variables
JOBS_left = list(range(1,maxjobs+1)) # name jobs 1,...,maxjobs
a_disc_list = ampl.getParameter('a_disc').getValues().toList()
mach_avail_time = [int(a_disc_list[i][1]) for i in range(5)]
proc_time_disc_list = ampl.getParameter('proc_time_disc').getValues().toList()
proc_time_disc = [int(proc_time_disc_list[i][1]) for i in range(maxjobs)]


# Heuristic
while (len(JOBS_left) > 0):
    machine = mach_avail_time.index(min(mach_avail_time)) # choose earliest available machine
    lambda_machine = []
    for i in JOBS_left:
        lambda_machine.append(lambda_mach[i-1][machine]) # extract lambda values for chosen machine
    
    job_ind = lambda_machine.index(max(lambda_machine))
    job = JOBS_left[job_ind] # find some job possible on chosen machine
    JOBS_left.pop(job_ind) # job performed -> remove from JOBS_left
    
    mach_avail_time[machine] += proc_time_disc[job_ind] # update available time for machine
