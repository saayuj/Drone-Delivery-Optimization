# Parameters
param grid_size;
param initial_final_points{i in 1..4};
param distance_matrix{i in 1..grid_size, j in 1..grid_size, k in 1..grid_size, l in 1..grid_size};

# Decision Variable
var nodes{i in 1..grid_size, j in 1..grid_size} binary;
var edges{i in 1..grid_size, j in 1..grid_size, k in 1..grid_size, l in 1..grid_size} binary;

# Objective Function
minimize Cost:
	sum{i in 1..grid_size, j in 1..grid_size, k in 1..grid_size, l in 1..grid_size} distance_matrix[i, j, k, l] * nodes[i, j] * nodes[k, l] / 2;

# Constraint 1 - Initial and Final Points should be 1
subject to Initial_and_Final_Points_One{i in 1..2}:
	nodes[initial_final_points[2 * i - 1], initial_final_points[2 * i]] = 1;
	
# Constraint 2 - Obstacles should be 0
subject to Obstacles_Zero{i in 1..obstacles_number}:
	nodes[obstacles[2 * i - 1], obstacles[2 * i]] = 0;

# Constraint 3 - Setting Edges 0 for Impossible Transitions
subject to Impossible_Edges_Zero{i in 1..grid_size, j in 1..grid_size, k in 1..grid_size, l in 1..grid_size}:
	edges[i, j, k, l]
	=
	(if ((k in i-1..i+1) and (l in j-1..j+1) and (k != i and l != j))
	then (nodes[i, j] * nodes[k, l])
	else (0)
	);

# Constraint 4 - Path should be Connected
subject to Path_Connected{i in 1..grid_size, j in 1..grid_size}:
	sum{k in 1..grid_size, l in 1..grid_size} edges[i, j, k, l] 
	= 
	(if (i = initial_final_points[1] and j = initial_final_points[2]) or 
    (i = initial_final_points[3] and j = initial_final_points[4])
    then (1 * nodes[i, j])
    else (2 * nodes[i, j])
    );