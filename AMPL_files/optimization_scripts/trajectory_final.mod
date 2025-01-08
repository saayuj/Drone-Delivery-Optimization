# Parameters
param grid_size;
param cost_per_hop;
param obstacles_number;
param battery_swapping_stations_number;
param initial_final_points{i in 1..4};
param obstacles{i in 1..(2*obstacles_number)};
param battery_swapping_stations{i in 1..(2*battery_swapping_stations_number)};
param battery_added{i in 1..grid_size, j in 1..grid_size};
param distance_matrix{i in 1..grid_size, j in 1..grid_size, k in 1..grid_size, l in 1..grid_size};

# Decision Variable
var nodes{i in 1..grid_size, j in 1..grid_size} binary;
var bss_visited{i in 1..grid_size, j in 1..grid_size} binary;

# Objective Function
minimize Cost:
	sum{i in 1..grid_size, j in 1..grid_size, k in 1..grid_size, l in 1..grid_size} distance_matrix[i, j, k, l] * nodes[i, j] * nodes[k, l] / 2;

# Constraint 1 - Initial and Final Points should be 1
subject to Initial_and_Final_Points_One{i in 1..2}:
	nodes[initial_final_points[2 * i - 1], initial_final_points[2 * i]] = 1;
	
# Constraint 2 - Obstacles should be 0
subject to Obstacles_Zero{i in 1..obstacles_number}:
	nodes[obstacles[2 * i - 1], obstacles[2 * i]] = 0;
	
# Constraint 3 - Define new Matrix d_ij which is intersection of Visited Points & BSS
subject to Form_Matrix_D{i in 1..grid_size, j in 1..grid_size}:
	bss_visited[i, j] = nodes[i, j] * battery_added[i, j] / 10;
    
# Constraint 4 - Path should be Connected
subject to Path_Connected{i in 1..grid_size, j in 1..grid_size}:
	if nodes[i, j] = 1
	then 
		if (2 <= i <= grid_size-1 and 2 <= j <= grid_size-1)
		then sum{k in i-1..i+1, l in j-1..j+1} nodes[k, l]
		
		else if (i = 1 and 2 <= j <= grid_size-1)
		then sum{k in i..i+1, l in j-1..j+1} nodes[k, l]
		
		else if (i = grid_size and 2 <= j <= grid_size-1)
		then sum{k in i-1..i, l in j-1..j+1} nodes[k, l]
		
		else if (2 <= i <= grid_size-1 and j = 1)
		then sum{k in i-1..i+1, l in j..j+1} nodes[k, l]
		
		else if (2 <= i <= grid_size-1 and j = grid_size)
		then sum{k in i-1..i+1, l in j-1..j} nodes[k, l]
		
		else if (i = 1 and j = 1)
		then sum{k in i..i+1, l in j..j+1} nodes[k, l]
		
		else if (i = 1 and j = grid_size)
		then sum{k in i..i+1, l in j-1..j} nodes[k, l]
		
		else if (i = grid_size and j = 1)
		then sum{k in i-1..i, l in j..j+1} nodes[k, l]
		
		else if (i = grid_size and j = grid_size)
		then sum{k in i-1..i, l in j-1..j} nodes[k, l]
	=
	if nodes[i, j] = 1
	then 
		if ((i = initial_final_points[1] and j = initial_final_points[2]) or (i = initial_final_points[3] and j = initial_final_points[4]))
		then 2
		else 3
	;
	
# Constraint 5 - Battery Level should be Positive at each Hop
subject to Battery_Level_Positive{i in 1..grid_size, j in 1..grid_size}:
	if (3 <= i <= grid_size-2 and 3 <= j <= grid_size-2)
	then sum{k in i-2..i+2, l in j-2..j+2} bss_visited[k, l]
	
	else if (i = 2 and 3 <= j <= grid_size-2)
	then sum{k in i-1..i+2, l in j-2..j+2} bss_visited[k, l]
	
	else if (i = 1 and 3 <= j <= grid_size-2)
	then sum{k in i..i+2, l in j-2..j+2} bss_visited[k, l]
	
	else if (i = grid_size-1 and 3 <= j <= grid_size-2)
	then sum{k in i-2..i+1, l in j-2..j+2} bss_visited[k, l]
	
	else if (i = grid_size and 3 <= j <= grid_size-2)
	then sum{k in i-2..i, l in j-2..j+2} bss_visited[k, l]
	
	else if (3 <= i <= grid_size-2 and j = 2)
	then sum{k in i-2..i+2, l in j-1..j+2} bss_visited[k, l]
	
	else if (3 <= i <= grid_size-2 and j = 1)
	then sum{k in i-2..i+2, l in j..j+2} bss_visited[k, l]
	
	else if (3 <= i <= grid_size-2 and j = grid_size-1)
	then sum{k in i-2..i+2, l in j-2..j+1} bss_visited[k, l]
	
	else if (3 <= i <= grid_size-2 and j = grid_size)
	then sum{k in i-2..i+2, l in j-2..j} bss_visited[k, l]
	
	else if (i = 1 and j = 1)
	then sum{k in i..i+2, l in j..j+2} bss_visited[k, l]
	
	else if (i = 1 and j = 2)
	then sum{k in i..i+2, l in j-1..j+2} bss_visited[k, l]
	
	else if (i = 2 and j = 1)
	then sum{k in i-1..i+2, l in j..j+2} bss_visited[k, l]
	
	else if (i = 2 and j = 2)
	then sum{k in i-1..i+2, l in j-1..j+2} bss_visited[k, l]
	
	else if (i = 1 and j = grid_size-1)
	then sum{k in i..i+2, l in j-2..j+1} bss_visited[k, l]
	
	else if (i = 1 and j = grid_size)
	then sum{k in i..i+2, l in j-2..j} bss_visited[k, l]
	
	else if (i = 2 and j = grid_size-1)
	then sum{k in i-1..i+2, l in j-2..j+1} bss_visited[k, l]
	
	else if (i = 2 and j = grid_size)
	then sum{k in i-1..i+2, l in j-2..j} bss_visited[k, l]
	
	else if (i = grid_size-1 and j = 1)
	then sum{k in i-2..i+1, l in j..j+2} bss_visited[k, l]
	
	else if (i = grid_size-1 and j = 2)
	then sum{k in i-2..i, l in j-1..j+2} bss_visited[k, l]
	
	else if (i = grid_size and j = 1)
	then sum{k in i-2..i, l in j..j+2} bss_visited[k, l]
	
	else if (i = grid_size and j = 2)
	then sum{k in i-2..i, l in j-1..j+2} bss_visited[k, l]
	
	else if (i = grid_size-1 and j = grid_size-1)
	then sum{k in i-2..i+1, l in j-2..j+1} bss_visited[k, l]
	
	else if (i = grid_size-1 and j = grid_size)
	then sum{k in i-2..i+1, l in j-2..j} bss_visited[k, l]
	
	else if (i = grid_size and j = grid_size-1)
	then sum{k in i-2..i, l in j-2..j+1} bss_visited[k, l]
	
	else if (i = grid_size and j = grid_size)
	then sum{k in i-2..i, l in j-2..j} bss_visited[k, l]
	>=
	if ((i = initial_final_points[1] and j = initial_final_points[2]) or (i = initial_final_points[3] and j = initial_final_points[4]))
    then 2 * bss_visited[i, j]
    else 3 * bss_visited[i, j]
    ;