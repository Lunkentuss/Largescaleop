reset;
#------------- Sets used in our model --------------
set K_mach_RESOURCES; 				# The set of MT-cells

#------------- Sets not used in our model ----------
set I_OP; 							# The sets of operations (1..5)
set K_RESOURCES; 					# The set of all machines
set Q_PREC; 						# First member of the set Q 

#------------- Param used in our model -------------
param T_HORIZON integer > 0 ; 		# Max number of intervals
param T_length_interval integer > 0;# Time in the discrete time intervals
param maxjobs integer > 0;			# Nbr of points	
param M > 0; 						# Big number (Not an integer)

set TIME = 0..T_HORIZON;
set JOBS = 1..maxjobs;

#------------- Param used in our model -------------

param proc_time_disc {JOBS}; 				# p_2j (or p_j in machining prob)
param p_j_o_postmach_disc {JOBS}; 			# p^(pmtilde), processing time p_2-n_j  
param a_disc {K_mach_RESOURCES}; 			# Time when resource k is available 
param r_disc {JOBS};						# Release date (machining problem)
param d_disc {JOBS};						# Due date (in hours)
param lambda_mach {JOBS,K_mach_RESOURCES}; 	# 1 if job j can be done in machine k 
											# 0 if job j can not be done in machine k

#------------ Param not used in our model ----------
param w >= 0;								# Transportation time between resources
param q_follow {Q_PREC}; 					# the pairs that form the set Q	
param v_jq {Q_PREC};
param v_disc_jq_ext {Q_PREC};
param v_mach_jq {Q_PREC};
param n {JOBS};
param proc_time_mach {JOBS};
param proc_time {I_OP,JOBS};
param p_postmach {JOBS};
param a {K_RESOURCES}; 						# Time when resource is ready
param r_mach {JOBS}; 						# Release date machining problem
param r {JOBS}; 							# Release date	
param d {JOBS};									
param lambda {I_OP,JOBS,K_RESOURCES};

#----------- Maybe used ---------------------------------
param resource_weight {JOBS};

