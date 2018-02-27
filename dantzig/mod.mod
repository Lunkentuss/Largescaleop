# Param names in data files: (which will will be used)
# a_disc := release data for resources 
# T_HORIZON := max number of time intervals
# T_length_interval := 1
# maxjobs := maximum number of jobs
# M := Big number >= planning horizon

# d_disc := due dates for the jobs
# proc_time_disc := processing time  (p_j in the MT-cell)
# p_j_o_postmach_disc := processing time (p^pmtilde, processing time 2-5)
# r_disc := release date for the machining problem

# Not used parameters:


param ind integer >= 0;

param row1 {j in 1..max(ind+1-1,ind)};  # Test max function

var x {j in 1..ind};

maximize fun: sum {j in 1..ind} row1[j] * x[j];

subject to constraintrow1 {j in 1..ind}: 0 <= x[j] <= 1;

subject to constraintxx {j in 1..ind}: x[j] <= 0.5; 

problem prob1: fun, x, constraintrow1;

problem prob2: fun, x, constraintrow1, constraintxx;
