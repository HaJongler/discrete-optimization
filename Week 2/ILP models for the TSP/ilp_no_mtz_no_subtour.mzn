% Define the problem's parameters
int: n;                                                                % number of vertices
array[1..(pow(2,n)-2)] of set of 1..n: subsets;                        % proper subsets of the vertices, excluding the empty set
array[1..n,1..n] of float: matrix;                                     % cost matrix
array[1..n,1..n] of var {0,1}: x;                                      % indicator of an edge existing in our TSP
var float: path_cost = sum(i,j in 1..n)(matrix[i,j] * x[i,j]);         % variable to be minimized

% Define our goal
solve minimize path_cost;
output ["\(path_cost)"];

% Define our constraints
constraint forall(i in 1..n)(
  sum([x[i,j] | j in 1..n]) = 2
);                                                                     % This constraint return h.c. and disjoint cycles

constraint forall(S in subsets)(
  sum([x[i,j] | i,j in 1..n where (i in S) /\ not(j in S)]) >= 1
);                                                                     % This constraint eliminates disjoint cycles