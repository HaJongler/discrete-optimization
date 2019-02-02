array[1..9, 1..9] of var 1..9: board = [|
_, 1, _, _, 6, _, _, _, _|
9, _, 2, _, _, 7, _, _, _|
_, 7, 5, _, _, _, _, 8, 2|
_, 8, _, _, _, _, 4, _, _|
_, _, _, 6, 2, 1, _, _, _|
_, _, 1, _, _, _, _, 3, _|
7, 9, _, _, _, _, 8, 1, _|
_, _, _, 9, _, _, 7, _, 5|
_, _, _, _, 7, _, _, 6, _|
|];

include "globals.mzn";

constraint 
  forall(i in 1..9)(
    alldifferent([board[i, j] | j in 1..9])
  );
constraint 
  forall(i in 1..9)(
    alldifferent([board[j, i] | j in 1..9])
  );
constraint 
  forall(i, j in 0..2)(
    alldifferent([board[br + (i * 3), bc + (j * 3)] | br, bc in 1..3])
  );


output [ "sudoku:\n" ] ++
    [ show(board[i,j]) ++
        if j = 9 then
            if i mod 3 = 0 /\ i < 9 then "\n\n" else "\n" endif
        else
            if j mod 3 = 0 then "  " else " " endif
        endif
| i,j in 1..9 ];

solve satisfy;