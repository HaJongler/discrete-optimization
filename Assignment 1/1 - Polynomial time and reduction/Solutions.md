# Problem 1
 Formulate the decision, evaluation and search variants of Set Cover, TSP and 0,1-Knapsack problems.
## Set Cover
####Decision
For a given finite collection of sets S whose union equals U, and a given number N, **tell whether exists** a sub-collection of S whose union equals U and whose size is l.t.e N.
####Evaluation
For a given finite collection of sets S whose union equals U, find the **cardinality of the smallest** sub-collection of S whose union equals U.
####Search
For a given finite collection of sets S whose union equals U, find the **smallest sub-collection** of S whose union equals U.

## TSP 
####Decision
For a given weighted graph G and a given number W **tell whether there exists** a Hamiltonian circuit of weight not exceeding W.
####Evaluation
For a given weighted graph G find the **minimal weight** of Hamiltonian circuits in G.
####Search
For a given weighted graph G find the **minimal hamiltonian circuit** in G.

## 0,1- Knapsack
####Decision
For a given set of items with different values and weights and a weight limit MW, **tell whether exists** a subset of items whose weight is l.t.e MW.
####Evaluation
For a given set of items with different values and weights and a weight limit MW, find the maximal value of a subset of items whose weight is l.t.e MW.
####Search
For a given set of items with different values and weights and a weight limit MW, find the subset of items whose value is maximal and whose weight is l.t.e MW.

# Problem 2
Prove that the Subset-Sum problem has a polynomial reduction to the Knapsack problem
## Solution
For every number a<sub>i</sub> in the given set S, create an item in the knapsack problem with value and weight equal to a<sub>i</sub>. Then, define the maximal weight for the knapsack solver as the wanted solution for the Subset-Sum problem (M). Since all the items in the knapsack problem have the save value-to-weight ratio (1), the best solution for a given M would be the subset of items that weigh exactly M. If we find such a solution, it means that there is a solution to the Subset-Sum problem, otherwise there is no solution.

# Problem 3
Show how you would use a solver for the evaluation variant of the [unweighted] Set Cover problem to create a solver for the search variant of the Set Cover.
##Solution
We run the solver for the evaluation variant N+1 times (where N = | S | ). First, we run the solver with all items, to find the optimal number of subsets. Then, we run the solver N more times, each time without one element of S. If the result is greater than the optimal solution, it means that we must include the set we just included in the optimal solution. If the result is equal to the optimal solution, it means that there is a set that can replace our set and with which we can still get an optimal solution, so now we have to do two things: 
1. We don't include the excluded set in the optimal solution.
2. Exclude the excluded set for all runs from now forward.



























