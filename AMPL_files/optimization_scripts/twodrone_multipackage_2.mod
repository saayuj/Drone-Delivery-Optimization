# Parameters
param grid_size;
param time;
param number_of_drones;
param number_of_delivery_location;
param warehouse_location{i in 1..(2 * number_of_drones)};
param delivery_location{i in 1..(2 * number_of_delivery_location)};
param delivery_demand{i in 1..number_of_delivery_location};
param net_demand;
param distance_matrix{i in 1..grid_size, j in 1..grid_size, k in 1..grid_size, l in 1..grid_size};

# Decision Variable
var nodes{n in 1..number_of_drones, i in 1..grid_size, j in 1..grid_size, t in 1..time} binary;
var flag{n in 1..number_of_drones, t in 1..time} binary;

# Objective Function
minimize Cost:
	sum{n in 1..number_of_drones, i in 1..grid_size, j in 1..grid_size, k in 1..grid_size, l in 1..grid_size, t in 1..time-1} distance_matrix[i, j, k, l] * nodes[n, i, j, t] * nodes[n, k, l, t + 1];
	
# Constraint 1 - Initial Point should be 1
subject to Initial_Point_One{n in 1..number_of_drones}:
	nodes[n, warehouse_location[2 * n - 1], warehouse_location[ 2 * n ], 1] = 1;
	
# Constraint 2 - Padded Points should be 0
subject to Padded_Points_Zero{n in 1..number_of_drones, i in 1..grid_size, j in 1..grid_size, t in 1..time}:
	if ((i = 1 and 1 <= j <= grid_size) or (i = grid_size and 1 <= j <= grid_size) or (j = 1 and 2 <= i <= grid_size - 1) or (j = grid_size and 2 <= i <= grid_size - 1))
	then nodes[n, i, j, t] = 0;

# Constraint 3 - Path should be Connected
subject to Path_Connected{n in 1..number_of_drones, i in 2..grid_size-1, j in 2..grid_size-1, t in 1..time-1}:
	if nodes[n, i, j, t] = 1 then sum{k in i-1..i+1, l in j-1..j+1} nodes[n, k, l, t+1] else 1 = 1;

# Constraint 4 - One Node should be 1 at a particular Time
subject to Sequential_Movement{n in 1..number_of_drones, t in 1..time}:
	sum{i in 1..grid_size, j in 1..grid_size} nodes[n, i, j, t] = 1;

# Constraint 5 - Collision Avoidance for drones 1 & 2
#subject to Collision_Avoidance_1{i in 2..grid_size-1, j in 2..grid_size-1, t in 1..time}:
#	nodes[1, i, j, t] * nodes[2, i, j, t] = 0;
	
# Constraint 0 - flag[0]=0
subject to Initial_Flag{n in 1..number_of_drones}:
	flag[n, 1] = 0;
	
# Constraint 6 - Flag Operation
subject to Flag_Check1{t in 1..time-1}:
	if flag[1, t] = 0
	then 
		if nodes[1, delivery_location[1], delivery_location[2], t+1]  = 1
		then (flag[1, t+1] - 1)
		else flag[1, t+1]
	=
	0;
	
/*subject to Flag_Check2{t in 1..time-1}:
	if flag[2, t] = 0
	then 
		if nodes[2, delivery_location[3], delivery_location[4], t+1]  = 1
		then (flag[2, t+1] - 1)
		else flag[2, t+1]
	=
	0;*/

# Constraint 7 - Flag Operation - Warehouse
subject to Flag_Check_1{t in 1..time-1}:
	if flag[1, t] = 1
	then 
		if nodes[1, warehouse_location[1], warehouse_location[2], t+1]  = 1
		then flag[1, t+1]
		else (1 - flag[1, t+1])
	=
	0;
	
/*subject to Flag_Check_2{t in 1..time-1}:
	if flag[2, t] = 1
	then 
		if nodes[2, warehouse_location[3], warehouse_location[4], t+1]  = 1
		then flag[2, t+1]
		else (1 - flag[2, t+1])
	=
	0;*/

# Constraint 8 -  Demand Satisfaction Warehouse
subject to Demand_Warehouse:
	sum{t in 1..time, n in 1..number_of_drones} (nodes[1, warehouse_location[2 * n - 1], warehouse_location[ 2 * n ],t] * (1 - flag[1, t])  + nodes[2, warehouse_location[2 * n - 1], warehouse_location[ 2 * n ],t] * (1 - flag[2, t])) = net_demand+4;

# Constraint 9 -  Demand Satisfaction Delivery_Location
subject to Demand_Delivery_Location{n in 1..number_of_delivery_location}:
	sum{t in 1..time} (nodes[1, delivery_location[2 * n - 1], delivery_location[2 * n],t] * flag[1, t] + nodes[2, delivery_location[2 * n - 1], delivery_location[2 * n],t] * flag[2, t]) = delivery_demand[n];

