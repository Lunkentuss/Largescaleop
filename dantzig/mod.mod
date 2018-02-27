# Param names in data files:
# a := release data for resources 
# T_HORIZON := max number of time intervals
# T_length_interval := 1
# maxjobs := maximum number of jobs
# M := Big number >= planning horizon
# d_disc := due dates for the jobs
# proc_time_disc := processing time 
# r_mach := release date for the machining problem


param ind integer >= 0;

param row1 {j in 1..ind}; 

var x {j in 1..ind};

maximize fun: sum {j in 1..ind} row1[j] * x[j];

subject to constraintrow1 {j in 1..ind}: 0 <= x[j] <= 1;

subject to constraintxx {j in 1..ind}: x[j] <= 0.5; 

problem prob1: fun, x, constraintrow1;

problem prob2: fun, x, constraintrow1, constraintxx;
