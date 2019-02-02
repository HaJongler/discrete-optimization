int: N = 30;

array[1..N] of var 1..N: x;

include "alldifferent.mzn";

% constraint forall(i,j in 1..N)(i != j -> x[i] != x[j]);
constraint alldifferent(x);  % super slow 
constraint forall(i,j in 1..N)(i < j -> abs(x[i] - x[j]) != j - i);
% WE CAN FLIP THE BOARD AND ITS THE SAME, ALSO WE CAN FLIP ON DIAGONAL. anyways, start on var with less choices.
constraint x[1] <= N / 2;

% output ["positions of queens are \(x)"];
% output ["(\(i), \(x[i])) " | i in 1..N];
output [if i < N then "(\(i), \(x[i])), " else "(\(i), \(x[i]))" endif | i in 1..N];

% solve satisfy;
% solve maximize(x[1] + 5 * x[2])
solve 
%   ::restart_geometric(1.1, 1)
  ::restart_luby(1)
  ::seq_search([
    int_search([x[1]], dom_w_deg, indomain_random, complete)
    ])
%   ::int_search(x, dom_w_deg, indomain_random, complete)
  satisfy;