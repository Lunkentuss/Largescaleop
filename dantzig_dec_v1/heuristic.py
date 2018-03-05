import sys
sys.path.append("../utils/")

from amplpy import AMPL
from getpara import *

def index_sorted(name_array,reverse=False):
	""" Returns a list of indices which is ordered
		by the values in the given name_array
	"""

	a = name_array.copy()
	sorted_index_list = [0 for x in range(len(a))]

	if(reverse):
		f = max
		maxmin = -sys.maxsize
	else:
		f = min
		maxmin = sys.maxsize 

	for i in range(len(a)):
		ind_max = a.index(f(a))
		sorted_index_list[i] = ind_max
		a[ind_max] = maxmin

	return sorted_index_list

def getDictHeuristic(ampl):
	# Initialization of parameters and variables
	mach_list = set2list(ampl,'K_mach_RESOURCES')
	nbr_of_machines = len(mach_list)
	maxjobs = getSingleParameter(ampl,'maxjobs')
	lambda_mach = flexdf2mat(ampl.getParameter('lambda_mach').getValues(),maxjobs,nbr_of_machines)
	a_disc_list = para2list(ampl,'a_disc')
	r_disc_list = para2list(ampl,'r_disc')
	proc_time_disc_list =  para2list(ampl,'proc_time_disc')
	T_HORIZON = getSingleParameter(ampl,'T_HORIZON')
	TIME = list(range(T_HORIZON+1))

	mach_avail_time = a_disc_list
	JOBS_left = list(range(maxjobs))
	x = {(x+1,y,z):0 for x in JOBS_left for y in mach_list for z in TIME}
	
	# Order after job time in descending order
	#JOBS_left = index_sorted(proc_time_disc_list,reverse=True)
	while (len(JOBS_left) > 0):
		mach_avail_time_ind_ord = index_sorted(mach_avail_time)

		break_loop = False
		for mach in mach_avail_time_ind_ord:
			for job in JOBS_left:
				# Test if job is feasible in machine
				if(lambda_mach[job][mach] == 1):
					#print(x[(job+1,mach_list[mach],mach_avail_time[mach])])
					#x[(job+1,mach_list[mach],mach_avail_time[mach])] = 1
					#print(x[(job+1,mach_list[mach],mach_avail_time[mach])])
					if(r_disc_list[job] <= mach_avail_time[mach]):
						x[(job+1,mach_list[mach],mach_avail_time[mach])] = 1
						mach_avail_time[mach] += proc_time_disc_list[job]
					else:
						x[(job+1,mach_list[mach],mach_avail_time[mach]+r_disc_list[job])] = 1
						mach_avail_time[mach] += proc_time_disc_list[job] + r_disc_list[job]
					JOBS_left.pop(JOBS_left.index(job))
					#print(JOBS_left)

					break_loop = True
				
				if(break_loop):
					break
			if(break_loop):
				break

	return x 

#if __name__ == '__main__':
#	print('OK')
