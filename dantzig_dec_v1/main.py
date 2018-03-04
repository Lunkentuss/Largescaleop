import sys
sys.path.append('../utils/')
from amplpy import AMPL, DataFrame
from getpara import *
from heuristic import getDictHeuristic

def main():

	ampl = AMPL()

	ampl.read('mod.mod')
	ampl.readData('dat.dat')
	ampl.setOption('solver','cplex')

	# Declare problems
	ampl.eval('problem lp_dual1: obj_LP_D_RMP, pi, gamma, constraint_d1;')
	ampl.eval('problem column_generation1: obj_sub, x_sub,constraint_s1,' +
				'constraint_s1, constraint_s3;')
	ampl.eval('problem rmp1: obj_rmp, tau, constraint_rmp1, constraint_rmp2;')
	ampl.eval('problem rmp1_bin: obj_rmp_bin, tau_bin, constraint_rmp1_bin, constraint_rmp2_bin;')

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
	A = [1 for x in range(nbr_of_jobs)]
	B = [0 for x in range(nbr_of_jobs)]
	setParamOfSingleSet(ampl,'JOBS','A',A)
	setParamOfSingleSet(ampl,'JOBS','B',B)

	#print("A-dict: " + str(ampl.getParameter('A').getValues().toDict()))
	#print("B-dict: " + str(ampl.getParameter('B').getValues().toDict()))

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

	#print(ampl.getParameter('x_heur').getValues().toDict())

	#print(heur_dict)
	#print('L_len := ' + str(getSingleParameter(ampl,'L_len')))


	# Calculate RMP for the feasible solution(objective value)


	# Loop for column generation
	max_iterations = 100;
	l = 1;
	while(True):
		# Debuggers:
		#print('L_len := ' + str(getSingleParameter(ampl,'L_len')))

		# Termination criteria == 1 (close enough criteria)
		if(l > max_iterations): 
			break;

		# Solve RMP (pessimistic bound)------------------------------
		# New problem decleration because strange problem

		ampl.eval('solve rmp1;')
		#ampl.eval('display tau;')

		print('== obj_rmp: ' + repr(ampl.getObjective('obj_rmp').value()))

		#ampl.eval('display pi;')
		#ampl.eval('display gamma;')

		# Optimistic bound??????

		# Solve dual RMP --------------------------------------------
		ampl.eval('solve lp_dual1;')

		# Increase l
		l = l + 1
		ampl.eval('let L_len := ' + repr(l) + ';')

		# Solve column generation problem and update x_bar-----------
		reduced_cost = column_gen(ampl,mach_list)
		
		if(isAllPositive(reduced_cost)):
			break


	# Solve RMP with binary constraint
	print(l)
	ampl.eval('solve rmp1_bin;')


def column_gen(ampl,mach_list):
	red_cost = [0 for x in range(len(mach_list))]

	for i in range(len(mach_list)):
		ampl.eval('reset data mach_k;')
		ampl.eval('data ; set mach_k := ' + mach_list[i] + ';')
		#print(set2list(ampl,'mach_k'))
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

	#print(red_cost)
	return red_cost

def isAllPositive(array):
	"""	Returns true if an array
	has only non-negative values
	"""

	for i in range(len(array)):
		if(array[i] < 0):
			return False
	return True 

if __name__ == '__main__':
	main()
