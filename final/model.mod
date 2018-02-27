#------------- Sets used in our model --------------
set K_mach_RESOURCES; 				# The set of MT-cells

#------------- Sets not used in our model ----------
set I_OP; 							# The sets of operations (1..5)
set K_RECOURCES; 					# The set of all machines
set Q_PREC; 						# 

#------------- Param used in our model -------------
param T_HORIZON integer > 0; 		# Max number of intervals
param T_length_interval integer > 0;# Time in the discrete time intervals
param maxjobs integer > 0;			# Nbr of points	
param M > 0; 						# Big number (Not an integer)

set TIME {1..T_HORIZON} > 0;
set JOBS {1..maxjobs} > 0;

#------------- Param used in our model -------------

param proc_time_disc {JOBS}; 				# p_2j (or p_j in machining prob)
param p_j_o_postmach_disc {JOBS}; 			# p^(pmtilde), processing time p_2-n_j  
param a_disc {K_mach_RESOURCES}; 			# Time when resource k is available 
param r_disc {JOBS};						# Release date (machining problem)
param d_disc {JOBS};						# Due date (in hours)
param lambda_mach {JOBS,K_mach_RESOURCES}; 	# 1 if job j can be done in machine k 
									# 0 if job j can not be done in machine k

#------------ Param not used in our model ----------
param w;						# Transportation time between resources
param q_follow; 				# the pairs that form the set Q	
param v_jq;
param v_disc_jq_ext;
param v_mach_jq;
param n;
param proc_time_mach;
param proc_time;
param p_postmach;
param a;
param r_mach;
param r;
param d;
param lambda;

#----------- Maybe used ---------------------------------
param resource_weight;


#---------- Program -------------------------------------
#set time = {1..maxjobs};
