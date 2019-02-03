int: n_elements;
int: n_sets;

array[1..n_sets] of int: 
  costs;
  
array[1..n_sets] of set of 0..n_elements-1: 
  sets;
  
array[1..n_sets] of var float: chosen;

constraint forall(i in 1..n_sets)((chosen[i] >= 0) /\ (chosen[i] <= 1));

constraint 
  forall(e in 0..n_elements-1)(
    sum([if e in sets[i] then chosen[i] else 0 endif | i in 1..n_sets]) >= 1
  );
  
var float
: 
  total_cost = 
    sum(i in 1..n_sets)(
      costs[i] * chosen[i]
    );

solve minimize total_cost;