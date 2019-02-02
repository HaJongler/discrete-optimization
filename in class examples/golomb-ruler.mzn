int: M = 10;
array[1..M] of var 0..100: a;

include "globals.mzn";

constraint increasing(a);
constraint alldifferent([a[j] - a[i] | i, j in 1..M where i < j]);
constraint a[1] = 0;

constraint a[2] - a[1] < a[M] - a[M-1];
% constraint forall(i in 2..(M - 1))(a[i + 1] - a[i] > a[i] - a[i - 1] /\ a[i] > a[i - 1]);
% constraint (a[M] = B);

solve minimize a[M];