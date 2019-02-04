% define matrix size
int: N = 20;
int: HN = N div 2;
% define matrix
array[1..N,1..N] of var -1..1: matrix;
include "globals.mzn"; 

% variables can only be 1 or -1:
constraint forall(i,j in 1..N)(matrix[i,j] != 0);

% All non diagonal elements are equal
constraint forall(i,j in 1..N where i != j)(
  matrix[i,j] = matrix[j,i]
  );

% First row and column have value of 1
constraint all_equal([matrix[1,i] | i in 1..N]);
constraint matrix[1,1] = 1;

% Exactly half of the elements are different
constraint forall(i in 1..N-1)(
  forall(k in i+1..N)(
    sum([if matrix[i,j] = matrix[k,j] then 1 else 0 endif | j in 1..N]) = HN
  )
);

% Order in decreasing binary values
constraint forall(i in 1..N-1)(
  sum([(if matrix[i,j] = 1 then 1 else 0 endif) * pow(2, N - j) | j in 1..N]) >
  sum([(if matrix[i+1,j] = 1 then 1 else 0 endif) * pow(2,N - j) | j in 1..N])
  );
  
% All dot products must be equal to zero
constraint forall(i in 1..N-1)(
  forall(j in i+1..N)(
    (sum([matrix[i,k] * matrix[j,k] | k in 1..N]) = 0)
  )
);

% output the matrix in nice format
output [ "matrix:\n" ] ++
    [ show_float(2, 0, matrix[i,j]) ++ 
      if j = N then "\n" else " " endif
      | i,j in 1..N ];

solve 
  ::restart_luby(1)
  ::seq_search([
    int_search(matrix, input_order, indomain_max, complete)
    ])
  satisfy;