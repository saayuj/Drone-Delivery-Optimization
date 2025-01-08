# Parameters
param grid_size;
param time;
param number_of_drones;
param obstacles_number;
param battery_swapping_stations_number;
param initial_final_points{i in 1..(4 * number_of_drones)};
param obstacles{i in 1..(2*obstacles_number)};
param battery_swapping_stations{i in 1..(2*battery_swapping_stations_number)};
param battery_added{i in 1..grid_size, j in 1..grid_size};
param distance_matrix{i in 1..grid_size, j in 1..grid_size, k in 1..grid_size, l in 1..grid_size};

# Decision Variable
var nodes{n in 1..number_of_drones, i in 1..grid_size, j in 1..grid_size, t in 1..time} binary;
var bss_visited{n in 1..number_of_drones, i in 1..grid_size, j in 1..grid_size, t in 1..time} binary;

# Objective Function
minimize Cost:
	sum{n in 1..number_of_drones, i in 1..grid_size, j in 1..grid_size, k in 1..grid_size, l in 1..grid_size, t in 1..time} nodes[n, i, j, t] * sqrt((i - initial_final_points[4 * n - 1])^2 + (j - initial_final_points[4 * n])^2);

# Constraint 1 - Initial Point should be 1
subject to Initial_Point_One{n in 1..number_of_drones}:
	nodes[n, initial_final_points[4 * n - 3], initial_final_points[4 * n - 2], 1] = 1;

# Constraint 2 - Padded Points should be 0
subject to Padded_Points_Zero{n in 1..number_of_drones, i in 1..grid_size, j in 1..grid_size, t in 1..time}:
	if ((i = 1 and 1 <= j <= grid_size) or (i = grid_size and 1 <= j <= grid_size) or (j = 1 and 2 <= i <= grid_size - 1) or (j = grid_size and 2 <= i <= grid_size - 1))
	then nodes[n, i, j, t] = 0;

# Constraint 3 - Obstacles should be 0
subject to Obstacles_Zero{n in 1..number_of_drones, i in 1..obstacles_number, t in 1..time}:
	nodes[n, obstacles[2 * i - 1], obstacles[2 * i], t] = 0;

# Constraint 4 - Define new Matrix d_ij which is intersection of Visited Points & BSS
subject to Form_Matrix_D{n in 1..number_of_drones, i in 1..grid_size, j in 1..grid_size, t in 1..time}:
	bss_visited[n, i, j, t] = nodes[n, i, j, t] * battery_added[i, j] / 10;

# Constraint 5 - Path should be Connected
subject to Path_Connected{n in 1..number_of_drones, i in 2..grid_size-1, j in 2..grid_size-1, t in 1..time-1}:
	if nodes[n, i, j, t] = 1
	then 
		if t = 1
		then sum{k in i-1..i+1, l in j-1..j+1, m in t..t+1} nodes[n, k, l, m]
		else sum{k in i-1..i+1, l in j-1..j+1, m in t-1..t+1} nodes[n, k, l, m]
	=
	if nodes[n, i, j, t] = 1
	then 
		if (i = initial_final_points[4 * n - 3] and j = initial_final_points[4 * n - 2])
		then 2
		else 3
	;

# Constraint 6 - One Node should be 1 at a particular Time
subject to Sequential_Movement{n in 1..number_of_drones, t in 1..time}:
	sum{i in 1..grid_size, j in 1..grid_size} nodes[n, i, j, t] = 1;

# Constraint 7 - Collision Avoidance for drones 1 & 2
subject to Collision_Avoidance_1{i in 2..grid_size-1, j in 2..grid_size-1, t in 2..time}:
	if nodes[1, i, j, t] = nodes[2, i, j, t] = 1
	then nodes[1, i, j, t] * nodes[2, i, j, t] = 0;

# Constraint 8 - Collision Avoidance for drones 2 & 3
subject to Collision_Avoidance_2{i in 2..grid_size-1, j in 2..grid_size-1, t in 2..time}:
	if nodes[2, i, j, t] = nodes[3, i, j, t] = 1
	then nodes[2, i, j, t] * nodes[3, i, j, t] = 0;

# Constraint 9 - Collision Avoidance for drones 3 & 1
subject to Collision_Avoidance_3{i in 2..grid_size-1, j in 2..grid_size-1, t in 2..time}:
	if nodes[1, i, j, t] = nodes[3, i, j, t] = 1
	then nodes[1, i, j, t] * nodes[3, i, j, t] = 0;

# Constraint 10 - Battery Level should be Positive at each Hop
#subject to Battery_Level_Positive{n in 1..number_of_drones, t in 1..time-3}:
#	if sum{i in 1..grid_size, j in 1..grid_size} bss_visited[n, i, j, t] = 1
#	then sum{i in 1..grid_size, j in 1..grid_size, k in t+1..t+3} bss_visited[n, i, j, k] >= 1
#	;