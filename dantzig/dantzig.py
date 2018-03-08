import sys
sys.path.append('../utils/')
from amplpy import AMPL, DataFrame
from getpara import *
from heuristic import getDictHeuristic
from time import time

def column_gen(ampl,mach_list):
	red_cost = [0 for x in range(len(mach_list))]

	for i in range(len(mach_list)):
		ampl.eval('reset data mach_k;')
		ampl.eval('data ; set mach_k := ' + mach_list[i] + ';')
		ampl.eval('solve column_generation1;')
		red_cost[i] = ampl.getObjective('obj_sub').value()

		# Eval x_bar_sum_u
		ampl.eval('let {l in L_len..L_len, j in JOBS, k in mach_k}' +
			  	'x_bar_sum_u[l,j,k]  := sum{u in TIME}(x_sub[j,k,u]);')
		# Eval x_bar_sum_u_star
		ampl.eval('let {l in L_len..L_len, k in mach_k}' +
			  	'x_bar_sum_u_star[l,k]  := sum{u in TIME, j in JOBS}' + 
				'((A[j]*(u+p_j_o_postmach_disc[j])+B[j]' + 
				'*max(u+p_j_o_postmach_disc[j]-d_disc[j],0))*x_sub[j,k,u]);')
		# Eval x_ljk
		ampl.eval('let {l in L_len..L_len, j in JOBS, k in mach_k} x_ljk[l,j,k] := sum{u in TIME}( (u+1)*x_sub[j,k,u] )-1;')

	#print(red_cost)
	return red_cost

def isAllPositive(array):
	"""	Returns true if an array
	has only non-negative values
	"""

	for i in range(len(array)):
		if(array[i] < -.0001):
			return False
	return True 

def extract_solution(x_ljk_dict,tau_bin_lk_dict,nbr_of_jobs,mach_list,l_size):
	list_sol = []
	for l in range(1,l_size+1):
		for mach in mach_list:
			for j in range(1,nbr_of_jobs+1):
				value = x_ljk_dict[(l,j,mach)]
				value = value[0]
				if(tau_bin_lk_dict[(mach,l)][0] == 1 and value != -1):
					list_sol.append((j,mach,value))

	return list_sol

def dantzig(ampl,A,B,data_path,max_iterations):

	ampl.setOption('solver','cplex')

	# Declare problems
	ampl.eval('problem lp_dual1: obj_LP_D_RMP, pi, gamma, constraint_d1;')
	ampl.eval('problem column_generation1: obj_sub, x_sub,constraint_s1,' +
				'constraint_s2, constraint_s3;')
	ampl.eval('problem rmp1: obj_rmp, tau, constraint_rmp1, constraint_rmp2;')
	ampl.eval('problem rmp1_bin: obj_rmp_bin, tau_bin, constraint_rmp1_bin, constraint_rmp2_bin;')

	# Get nbr of machines and the set 
	mach_list = set2list(ampl,'K_mach_RESOURCES')
	nbr_of_machines = len(mach_list)

	## Get the nbr of max jobs
	nbr_of_jobs = getSingleParameter(ampl,'maxjobs')
	nbr_of_jobs = int(nbr_of_jobs)

	# Set A[j] and B[j]
	setParamOfSingleSet(ampl,'JOBS','A',A)
	setParamOfSingleSet(ampl,'JOBS','B',B)

	# Find feasible solution from heuristic and set x[1,k,j]
	# in ampl
	ampl.eval('let L_len := 1;')
	heur_dict = getDictHeuristic(ampl)
	heur_df = DataFrame(('JOBS','K_mach_RESOURCES','TIME'),('x_heur'))
	heur_df.setValues(heur_dict)
	ampl.setData(heur_df)

	# Eval x_bar_sum_u
	ampl.eval('let {l in L_len..L_len, j in JOBS, k in K_mach_RESOURCES}' +
			  	'x_bar_sum_u[l,j,k]  := sum{u in TIME}(x_heur[j,k,u]);')
	# Eval x_bar_sum_u_star
	ampl.eval('let {l in L_len..L_len, k in K_mach_RESOURCES}' +
			  	'x_bar_sum_u_star[l,k]  := sum{u in TIME, j in JOBS}' + 
				'((A[j]*(u+p_j_o_postmach_disc[j])+B[j]' + 
				'*max(u+p_j_o_postmach_disc[j]-d_disc[j],0))*x_heur[j,k,u]);')
	# Eval x_ljk
	ampl.eval('let {l in L_len..L_len, j in JOBS, k in K_mach_RESOURCES} x_ljk[l,j,k] := sum{u in TIME}((u+1)*x_heur[j,k,u])-1;')

	# Loop for column generation
	l = 1;
	upper_bound = []
	start = time()
	time_iter = []

	while(True):
		# Debuggers:
		#print('L_len := ' + str(getSingleParameter(ampl,'L_len')))

		if(l > max_iterations): 
			break;

		# Solve dual RMP (Pessimistic bound) ------------------------
		ampl.eval('solve lp_dual1;')
		upper_bound.append(ampl.getObjective('obj_LP_D_RMP').value())

		time_iter.append(time()-start)

		# Increase l
		l = l + 1
		ampl.eval('let L_len := ' + repr(l) + ';')

		# Solve column generation problem and update x_bar-----------
		reduced_cost = column_gen(ampl,mach_list)
		
		if(isAllPositive(reduced_cost)):
			break


	# Solve RMP with binary constraint
	l = l - 1
	print("L : " + str(l))
	ampl.eval('solve rmp1_bin;')
	optimal = ampl.getObjective('obj_rmp_bin').value()
	upper_bound.append(optimal)
	time_iter.append(time()-start)

	# Extract x from x_ljk and tau_bin

	ampl.eval('display tau_bin;')
	x_rep = extract_solution(ampl.getParameter('x_ljk').getValues().toDict(),
							 ampl.getVariable('tau_bin').getValues().toDict(),
							 nbr_of_jobs,
							 mach_list,
							 l)
	return (x_rep,upper_bound,time_iter)
