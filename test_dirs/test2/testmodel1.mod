set P;

param nbr integer >= 0;

param line {j in 1..nbr};

param b {j in 1..nbr};
param c {j in 1..nbr};
param up {j in 1..nbr};

var X {j in 1..nbr};

maximize profit: sum {j in 1..nbr} c[j] * X[j];
subject to limit {j in 1..nbr}: 0 <= X[j] <= up[j];

# Matrix in dantzig test

subject to c1 {j in 1..nbr}: X[j] * line[j] <= 10; 
