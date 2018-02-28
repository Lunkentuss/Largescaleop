var x {JOBS,K_mach_RESOURCES,TIME} binary;

#---------- Objective function --------------------------
#minimize Finish_times_and_tardiness:
#sum {j in JOBS, k in K_mach_RESOURCES, u in TIME} (A[j]*(u+p_j_o_postmach_disc[j])+B[j]*max(u+p_j_o_postmach_disc[j]-d_disc[j],0))*x[j,k,u];

minimize Finish_times_and_tardiness:
sum{j in JOBS, k in K_mach_RESOURCES, u in TIME} (u + p_j_o_postmach_disc[j] + max(u + p_j_o_postmach_disc[j] - d_disc[j],0) ) * x[j,k,u];

#---------- Constraints ---------------------------------
subject to constraint1 {j in JOBS}:
        sum{k in K_mach_RESOURCES, u in TIME} x[j,k,u] = 1;

subject to constraint2 {j in JOBS, k in K_mach_RESOURCES}:
        sum{u in TIME} x[j,k,u] <= lambda_mach[j,k];

subject to constraint3 {k in K_mach_RESOURCES, u in TIME}:
        sum{j in JOBS, v in max(u-proc_time_disc[j]+1,0)..u} x[j,k,v] <= 1;

subject to constraint4 {j in JOBS, k in K_mach_RESOURCES, u in 0..max(r_disc[j],a_disc[k])}:
        x[j,k,u]=0;
