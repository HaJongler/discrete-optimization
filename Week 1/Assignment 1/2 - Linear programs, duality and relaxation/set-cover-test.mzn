int: n_elements;
int: n_sets;

array[1..n_sets] of int: 
  costs;
  
array[1..n_sets] of set of 0..n_elements-1: 
  sets;

array[1..n_sets] of var bool: 
  chosen;

constraint 
  forall(e in 0..n_elements-1)(
    exists(i in 1..n_sets where chosen[i])(
      e in sets[i]
    )
  );

var int: 
  total_cost = 
    sum(i in 1..n_sets where chosen[i])(
      costs[i]
    );
    
    output ["\(total_cost)"];

solve minimize total_cost;