int: n_items;
int: weight_limit;

array[1..n_items] of int: value;
array[1..n_items] of int: weight;

array[1..n_items] of var 0..1: chosen;
var int: total_value = sum([chosen[i] * value[i] | i in i..n_items]);

constraint sum([chosen[i] * weight[i] | i in i..n_items]) <= weight_limit;

output chosen;

solve satisfy;