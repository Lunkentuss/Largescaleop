import sys
sys.path.append("../utils/")

from amplpy import AMPL
from typing import NewType
from getpara import *

def getDictHeuristic(ampl):

	# Initialization of parameters and variables
	mach_list = set2list(ampl,'K_mach_RESOURCES')
	nbr_of_machines = len(mach_list)
	maxjobs = int(getSingleParameter(ampl,'maxjobs'))
	lambda_mach = flexdf2mat(ampl.getParameter('lambda_mach').getValues(),maxjobs,nbr_of_machines)
	a_disc_list = ampl.getParameter('a_disc').getValues().toList()
	mach_avail_time = [int(a_disc_list[i][1]) for i in range(nbr_of_machines)]
	proc_time_disc_list = ampl.getParameter('proc_time_disc').getValues().toList()
	proc_time_disc = [int(proc_time_disc_list[i][1]) for i in range(maxjobs)]
	T_HORIZON = int(getSingleParameter(ampl,'T_HORIZON'))
	TIME = list(range(0,T_HORIZON+1))
	#x = [[[0] * T_HORIZON for i in range(nbr_of_machines)] for j in range(maxjobs)]
	x = {(x,y,z):0 for x in mach_list for y in JOBS_left for z in TIME}

	JOBS_left = list(range(1,maxjobs+1)) # name jobs 1,...,maxjobs
	# Heuristic
	# Check if the job is ready and if the job can be done on the machine
	while (len(JOBS_left) > 0):
		mach_avail_time_ord = [mach_avail_time.index(x) for x in sorted(mach_avail_time)]
		for mach in mach_avail_time_ord:
			for job in JOBS_left:
				



    	lambda_machine = []
    	for i in JOBS_left:
        	lambda_machine.append(lambda_mach[i-1][machine]) # extract lambda values for chosen machine
    
    	job_ind = lambda_machine.index(max(lambda_machine))
    	job = JOBS_left[job_ind] # find some job possible on chosen machine
    
        X[job-1][machine][mach_avail_time[machine]] = 1

    	JOBS_left.pop(job_ind) # job performed -> remove from JOBS_left
    
    	mach_avail_time[machine] += proc_time_disc[job_ind] # update available time for machine
	return x 

# sorted(a,reverse=True)
# sorted(a)
