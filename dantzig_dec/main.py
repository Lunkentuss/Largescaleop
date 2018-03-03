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
	B = [1 for x in range(nbr_of_jobs)]
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
	max_iterations = 2;
	l = 2;
	ampl.eval('let L_len := 2;')
	while(1):
		# Debuggers:
		#print('L_len := ' + str(getSingleParameter(ampl,'L_len')))

		# Termination criteria == 1 (close enough criteria)
		if(1 != 1 or l >= max_iterations): 
			break;

		# Solve dual RMP

		# Solve column generation problem and update x_bar

		# Solve RMP (pessimistic bound)

		# Optimistic bound??????
	
		# Increase l
		l = l + 1;
		ampl.eval('let L_len := ' + repr(l) + ';')

	# Solve RMP with binary constraint



if __name__ == '__main__':
	main()
