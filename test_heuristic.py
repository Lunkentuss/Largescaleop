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

# Initialization of parameters and variables
maxjobs = int(getSingleParameter(ampl,'maxjobs'))
lambda_mach = flexdf2mat(ampl.getParameter('lambda_mach').getValues(),maxjobs,5)

JOBS_left = list(range(1,maxjobs+1)) # name jobs 1,...,maxjobs
a_disc_list = ampl.getParameter('a_disc').getValues().toList()
mach_avail_time = [int(a_disc_list[i][1]) for i in range(5)]
proc_time_disc_list = ampl.getParameter('proc_time_disc').getValues().toList()
proc_time_disc = [int(proc_time_disc_list[i][1]) for i in range(maxjobs)]
x = [[0] * 5 for i in range(maxjobs)]

# Heuristic
while (len(JOBS_left) > 0):
    machine = mach_avail_time.index(min(mach_avail_time)) # choose earliest available machine
    lambda_machine = []
    for i in JOBS_left:
        lambda_machine.append(lambda_mach[i-1][machine]) # extract lambda values for chosen machine
    
    job_ind = lambda_machine.index(max(lambda_machine))
    job = JOBS_left[job_ind] # find some job possible on chosen machine
    x[job-1][machine]=1 # allot job to machine
    JOBS_left.pop(job_ind) # job performed -> remove from JOBS_left
    
    mach_avail_time[machine] += proc_time_disc[job_ind] # update available time for machine

total_time = mach_avail_time[mach_avail_time.index(max(mach_avail_time))]
print(x)
print(total_time)
