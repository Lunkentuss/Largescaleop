set P;

param testint {j in P} integer >= 0;

param a {j in P};
param b;
param c {j in P};
param u {j in P};

var X {j in P};

maximize profit: sum {j in P} c[j] * X[j] * testint[j];
subject to time: sum {j in P} (1/a[j]) * X[j] <= b;
subject to limit {j in P}: 0 <= X[j] <= u[j];
