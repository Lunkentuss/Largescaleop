param ind integer >= 0;

param row1 {j in 1..ind}; 

var x {j in 1..ind};

maximize fun: sum {j in 1..ind} row1[j] * x[j];

subject to constraintrow1 {j in 1..ind}: 0 <= x[j] <= 1;

subject to constraintxx {j in 1..ind}: x[j] <= 0.5; 

problem prob1: fun, x, constraintrow1;

problem prob2: fun, x, constraintrow1, constraintxx;
