reset;
#------------- Sets used in our model ------------------
set K_mach_RESOURCES ; 				# The set of MT-cells

#------------- Sets not used in our model --------------
set I_OP; 							# The sets of operations (1..5)
set K_RESOURCES; 					# The set of all machines
set Q_PREC; 						# First member of the set Q 

#------------- Param used in our model -----------------
param T_HORIZON integer > 0 ; 		# Max number of intervals
param T_length_interval integer > 0;# Time in the discrete time intervals
param maxjobs integer > 0;			# Nbr of points	
param M > 0; 						# Big number (Not an integer)

set TIME = 0..T_HORIZON;
set JOBS = 1..maxjobs;

#------------- Param used in our model -----------------

param proc_time_disc {JOBS}; 				# p_2j (or p_j in machining prob)
param p_j_o_postmach_disc {JOBS}; 			# p^(pmtilde), processing time p_2-n_j  
param a_disc {K_mach_RESOURCES}; 			# Time when resource k is available 
param r_disc {JOBS};						# Release date (machining problem)
param d_disc {JOBS};						# Due date (in hours)
param lambda_mach {JOBS,K_mach_RESOURCES}; 	# 1 if job j can be done in machine k 
											# 0 if job j can not be done in machine k

#------------ Param not used in our model --------------
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

#----------- Maybe used --------------------------------
param resource_weight {JOBS};

# ======================================================
# ======================================================
# ======== Variables, constraints and objective ========
# ======================================================
# ======================================================


# ================ Script params ======================= 
param A{JOBS};
param B{JOBS};

# Column generation parameter:
param L_len := 1;

# Column generation parameter:
# Summation of x_bar over time
param x_bar_sum_u {1..L_len,JOBS,K_mach_RESOURCES};

# Column generation parameter:
# Summation of x_bar (A[j](u + p_j^pm) + B[j][u + p[j]j^pm - d[j]]_+)
param x_bar_sum_u_star {1..L_len,JOBS,K_mach_RESOURCES};

# ================ Primal problem ====================== 
var x {JOBS,K_mach_RESOURCES,TIME} binary;

#---------- Objective function -------------------------
minimize Finish_times_and_tardiness:
	sum {j in JOBS, k in K_mach_RESOURCES, u in TIME} (A[j]*(u+p_j_o_postmach_disc[j])+B[j]*max(u+p_j_o_postmach_disc[j]-d_disc[j],0))*x[j,k,u];

#---------- Constraints --------------------------------
subject to constraint_p1 {j in JOBS}:
	sum{k in K_mach_RESOURCES, u in TIME} x[j,k,u] = 1;

subject to constraint_p2 {j in JOBS, k in K_mach_RESOURCES}:
	sum{u in TIME} x[j,k,u] <= lambda_mach[j,k];

subject to constraint_p3 {k in K_mach_RESOURCES, u in TIME}:
	sum{j in JOBS, v in max(u-proc_time_disc[j]+1,0)..u} x[j,k,v] <= 1;

subject to constraint_p4 {j in JOBS, k in K_mach_RESOURCES, u in 0..max(r_disc[j],a_disc[k])}:
        x[j,k,u]=0;

#---------- Problem ------------------------------------
problem primal: Finish_times_and_tardiness, x, constraint_p1, 
				constraint_p2, constraint_p3, constraint_p4;

# ================ LP D-RMP  =========================== 
var pi {JOBS};
var gamma {K_mach_RESOURCES};

#---------- Objective function -------------------------
maximize obj_LP_D_RMP: 
	sum{j in JOBS} pi[j] + sum{k in K_mach_RESOURCES} gamma[k];
	
#---------- Constraints --------------------------------
subject to constraint_d1 {l in 1..L_len,k in K_mach_RESOURCES}:
	(sum{j in JOBS}x_bar_sum_u[l,j,k] * pi[j]) + gamma[k]  <= sum{j in JOBS} x_bar_sum_u_star[l,j,k]; # Summation problem?
		
#---------- Problem ------------------------------------
problem lp_dual: obj_LP_D_RMP, pi, gamma, constraint_d1;

# ================ *********  =========================== 