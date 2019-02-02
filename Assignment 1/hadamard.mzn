% define matrix size
int: N = 20;
% define matrix
array[1..N,1..N] of var -1..1: matrix;
% define the dot product variables
array[1..N-1] of var int: rows = [sum([matrix[i,j] * matrix[i+1,j] | j in 1..N]) | i in 1..N-1];   
array[1..N-1] of var int: cols = [sum([matrix[i,j] * matrix[i,j+1] | i in 1..N]) | j in 1..N-1];

include "globals.mzn"; 

% variables can only be 1 or -1:
constraint forall(i,j in 1..N)(matrix[i,j] != 0);
% All dot products should be equal to zero
constraint all_equal(rows); 
constraint rows[1] = 0;
constraint all_equal(cols); 
constraint cols[1] = 0;

% output the matrix in nice format
output [ "matrix:\n" ] ++
    [ show_float(2, 0, matrix[i,j]) ++ 
      if j = N then "\n" else " " endif
      | i,j in 1..N ];

solve 
  ::restart_luby(1)
  satisfy;