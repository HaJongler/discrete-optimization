int: B = 8;
array[1..B , 1..B] of var 0..1: board;

array[1..B,1..B] of var int: s = array2d(1..B, 1..B, [sum([board[x+dx , y+dy] | dx, dy in -1..1 
     where ((B >= x + dx) /\ (x + dx >= 1) /\ 
            (B >= y + dy) /\ (y + dy >= 1) /\ 
            ((dx != 0) \/ (dy != 0)))]) | x,y in 1..B]);

constraint
  forall(x,y in 1..B where board[x,y] = 1)(
    (s[x,y] = 3) \/ (s[x,y] = 2)
  );

solve 
  ::restart_luby(1)
  maximize sum([board[x, y] | x,y in 1..B]);