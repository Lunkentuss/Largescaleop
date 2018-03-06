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


# ================ Script parameters ===================
# ======================================================
param A{JOBS};
param B{JOBS};

param x_heur {JOBS,K_mach_RESOURCES,TIME};

# Column generation parameter:
param L_len integer;
set L = 1..L_len;

param x_ljk {L,JOBS,K_mach_RESOURCES};

# Column generation parameter:
# Summation of x_bar over time
param x_bar_sum_u {L,JOBS,K_mach_RESOURCES};

# Column generation parameter:
# Summation of x_bar (A[j](u + p_j^pm) + B[j][u + p[j]j^pm - d[j]]_+)
# over TIME and JOBS
param x_bar_sum_u_star {L,K_mach_RESOURCES};

# This set will always be set to one specific machine
# and is used in the column generation problem for 
# machine k
set mach_k within {K_mach_RESOURCES};

# ================ Primal problem ====================== 
# ======================================================
var x {JOBS,K_mach_RESOURCES,TIME} binary;

#---------- Objective function -------------------------
minimize Finish_times_and_tardiness:
	sum {j in JOBS, k in K_mach_RESOURCES, u in TIME} (A[j]*(u+p_j_o_postmach_disc[j])+B[j]*max(u+p_j_o_postmach_disc[j]-d_disc[j],0))*x[j,k,u];

#---------- Constraints --------------------------------
subject to constraint_p1 {j in JOBS}:
	sum{k in K_mach_RESOURCES, u in TIME} x[j,k,u] == 1;

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
# ======================================================
var pi {JOBS};
var gamma {K_mach_RESOURCES};

#---------- Objective function -------------------------
maximize obj_LP_D_RMP: 
	sum{j in JOBS}( pi[j] ) + sum{k in K_mach_RESOURCES}( gamma[k] );
	
#---------- Constraints --------------------------------
subject to constraint_d1 {l in L,k in K_mach_RESOURCES}:
	sum{j in JOBS}(x_bar_sum_u[l,j,k] * pi[j]) + gamma[k]  <= x_bar_sum_u_star[l,k]; # Summation problem goes where?
		
#---------- Problem ------------------------------------
problem lp_dual: obj_LP_D_RMP, pi, gamma, constraint_d1;

# ======== The column generation sub-problem  ==========
# ======================================================
var x_sub {JOBS,K_mach_RESOURCES,TIME} binary;

#---------- Objective function -------------------------
minimize obj_sub: sum{k in mach_k}(sum{j in JOBS,u in TIME}(
	(A[j]*(u+p_j_o_postmach_disc[j]) + B[j]*max(u+p_j_o_postmach_disc[j]-d_disc[j],0) - pi[j])*x_sub[j,k,u]) - gamma[k]); 

#---------- Constraints --------------------------------
subject to constraint_s1{j in JOBS, k in mach_k}:sum{u in TIME}(x_sub[j,k,u]) <= lambda_mach[j,k];

subject to constraint_s2 {k in mach_k, u in TIME}:
	sum{j in JOBS, v in max(u-proc_time_disc[j] + 1,0)..u} x_sub[j,k,v] <= 1;

subject to constraint_s3 {j in JOBS, k in mach_k, u in 0..max(r_disc[j],a_disc[k])}:
        x_sub[j,k,u] == 0;

#---------- Problem ------------------------------------
problem column_generation: obj_sub, x_sub,constraint_s1, constraint_s1, constraint_s3;

# ======================= RMP ==========================
# ======================================================
var tau{K_mach_RESOURCES,L} >= 0;

#---------- Objective function -------------------------
minimize obj_rmp: sum{l in L,k in K_mach_RESOURCES}(x_bar_sum_u_star[l,k] * tau[k,l]);

#---------- Constraints --------------------------------
subject to constraint_rmp1 {j in JOBS}: sum{k in K_mach_RESOURCES, l in L}(x_bar_sum_u[l,j,k] * tau[k,l]) = 1;

subject to constraint_rmp2 {k in K_mach_RESOURCES}: sum{l in L}(tau[k,l]) = 1;

#---------- Problem ------------------------------------
problem rmp: obj_rmp, tau, constraint_rmp1, constraint_rmp2;

# ======================= RMP-binary ===================
# ======================================================
var tau_bin{K_mach_RESOURCES,1..L_len-1} binary;

#---------- Objective function -------------------------
minimize obj_rmp_bin: sum{l in 1..L_len-1,k in K_mach_RESOURCES}(x_bar_sum_u_star[l,k] * tau_bin[k,l]);

#---------- Constraints --------------------------------
subject to constraint_rmp1_bin {j in JOBS}: sum{k in K_mach_RESOURCES, l in 1..L_len-1}(x_bar_sum_u[l,j,k] * tau_bin[k,l]) = 1;

subject to constraint_rmp2_bin {k in K_mach_RESOURCES}: sum{l in 1..L_len-1}(tau_bin[k,l]) = 1;

#---------- Problem ------------------------------------
problem rmp_bin: obj_rmp_bin, tau_bin, constraint_rmp1_bin, constraint_rmp2_bin;
