int: n_items;
int: weight_limit;

array[1..n_items] of int: value;
array[1..n_items] of int: weight;

array[1..n_items] of var 0..1: chosen;
var int: total_value = sum([chosen[i] * value[i] | i in 1..n_items]);

constraint sum([chosen[i] * weight[i] | i in 1..n_items]) <= weight_limit;

output [ "\(total_value)" ];

solve maximize total_value;