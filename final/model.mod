#------------- Param and sets used in model -------------
param T_HORIZON; 				# Max number of intervals
param T_length_interval;		# Time in the discrete time intervals
param maxjobs;					# Nbr of points	
param M; 						# Big number (Not an integer)

param proc_time_disc; 			# p_2j (or p_j in machining prob)
param p_j_o_postmach_disc; 		# p^(pmtilde), processing time p_2-n_j  
param a_disc; 					# Time when resource k is available 
param r_disc;					# Release date (machining problem)
param d_disc;					# Due date (in hours)
param lambda_mach; 				# 1 if job j can be done in machine k 
								# 0 if job j can not be done in machine k

#------------ Param and sets not used in model ----------
set I_OP;
set K_RESOURCES;
set K_mach_RESOURCES;
param w;
set Q_PREC;
param q_follow;
param v_jq;
param v_disc_jq_ext;
param v_mach_jq;
param n;
param proc_time_mach;
param p_postmach;
param a;
param r_mach;
param r;
param d;
param lambda;

#----------- Maybe used ---------------------------------
param resource_weight;

set time = {1..maxjobs};
