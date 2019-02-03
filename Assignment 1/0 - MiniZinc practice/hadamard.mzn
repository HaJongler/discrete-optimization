% define matrix size
int: N = 16;
int: HN = N div 2;
% define matrix
array[1..N,1..N] of var -1..1: matrix;
include "globals.mzn"; 

% variables can only be 1 or -1:
constraint forall(i,j in 1..N)(matrix[i,j] != 0);
% Using sylvester's trick
constraint forall(i,j in 1..HN)(
  (matrix[i, j] = matrix[i, j + HN]) /\
  (matrix[i, j] = matrix[i + HN, j]) /\
  (matrix[i, j] = - matrix[i + HN, j + HN])
  );
% All non diagonal elements are equal
constraint forall(i,j in 1..HN where i != j)(
  matrix[i,j] = matrix[j,i]
  );
% All dot products should be equal to zero
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
  satisfy;