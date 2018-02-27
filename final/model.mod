var x {JOBS,K_mach_RESOURCES,TIME} binary;

#---------- Objective function --------------------------
minimize Finish_times_and_tardiness:
sum {j in JOBS, k in K_mach_RESOURCES, u in TIME} (A[j]*(u+p_j_o_postmach_disc)+B[j]*max(u+p_j_o_postmach_disc-d_disc,0)*x[j,k,u];

#---------- Constraints ---------------------------------
subject to constraint1 {j in JOBS}:
        sum{k in K_mach_resources, u in TIME} x[j,k,u] = 1;

subject to constraint2 {j in JOBS, k in K_mach_RESOURCES}:
        sum{u in TIME} x[j,k,u] <= lambda[j,k];

subject to constraint3 {k in K_mach_RESOURCES, u in TIME}:
        sum{j in JOBS, v in max(u-proc_time_disc+1,0)..u} x[j,k,v] <= 1;

subject to constraint4 {u in 0..max(r_disc,a_disc)-1, j in JOBS, k in K_mach_RESOURCES}:
        x[j,k,u]=0;
