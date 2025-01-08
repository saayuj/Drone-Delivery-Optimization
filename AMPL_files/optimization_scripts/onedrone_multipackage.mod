# Parameters
param grid_size;
param time;
param number_of_delivery_location;
param warehouse_location{i in 1..2};
param delivery_location{i in 1..(2 * number_of_delivery_location)};
param delivery_demand{i in 1..number_of_delivery_location};
param net_demand;
param distance_matrix{i in 1..grid_size, j in 1..grid_size, k in 1..grid_size, l in 1..grid_size};

# Decision Variable
var nodes{i in 1..grid_size, j in 1..grid_size, t in 1..time} binary;
var flag{t in 1..time} binary;

# Objective Function
minimize Cost:
	sum{i in 1..grid_size, j in 1..grid_size, k in 1..grid_size, l in 1..grid_size, t in 1..time-1} distance_matrix[i, j, k, l] * nodes[i, j, t] * nodes[k, l, t + 1];
#	sum{i in 1..grid_size, j in 1..grid_size, t in 1..time, n in 1..number_of_delivery_location} (nodes[i, j, t] * (sqrt((i - delivery_location[2 * n - 1])^2 + (j - delivery_location[2 * n])^2) * (1 - flag[t]) + sqrt((i - warehouse_location[1])^2 + (j - warehouse_location[2])^2) * flag[t]));

# Constraint 1 - Initial Point should be 1
subject to Initial_Point_One:
	nodes[warehouse_location[1], warehouse_location[2], 1] = 1;

# Constraint 2 - Padded Points should be 0
subject to Padded_Points_Zero{i in 1..grid_size, j in 1..grid_size, t in 1..time}:
	if ((i = 1 and 1 <= j <= grid_size) or (i = grid_size and 1 <= j <= grid_size) or (j = 1 and 2 <= i <= grid_size - 1) or (j = grid_size and 2 <= i <= grid_size - 1))
	then nodes[i, j, t] = 0;

# Constraint 3 - Path should be Connected
subject to Path_Connected{i in 2..grid_size-1, j in 2..grid_size-1, t in 1..time-1}:
	if nodes[i, j, t] = 1 then sum{k in i-1..i+1, l in j-1..j+1} nodes[k, l, t+1] else 1 = 1;

# Constraint 4 - One Node should be 1 at a particular Time
subject to Sequential_Movement{t in 1..time}:
	sum{i in 1..grid_size, j in 1..grid_size} nodes[i, j, t] = 1;

# Constraint 5 - Flag initialized to 0
subject to Initial_Flag:
	flag[1] = 0;

# Constraint 6 - Flag Operation for Delivery
subject to Flag_Check1{t in 1..time-1}:
	if flag[t] = 0
	then 
		if (sum{n in 1..number_of_delivery_location} nodes[delivery_location[2 * n - 1], delivery_location[2 * n], t + 1] = 1)
		then (flag[t + 1] - 1)
		else flag[t + 1]
	=
	0;

# Constraint 7 - Flag Operation for returning to Warehouse
subject to Flag_Check_1{t in 1..time-1}:
	if flag[t] = 1
	then 
		if nodes[warehouse_location[1], warehouse_location[2], t + 1]  = 1
		then flag[t + 1]
		else (1 - flag[t + 1])
	=
	0;

# Constraint 8 - Supply Satisfaction Warehouse
subject to Supply_Warehouse:
	sum{t in 1..time} nodes[warehouse_location[1], warehouse_location[2], t] * (1 - flag[t]) = net_demand;

# Constraint 9 - Demand Satisfaction Delivery Location
/*subject to Demand_Delivery_Location{t in 1..time-1, n in 1..number_of_delivery_location}:
	if nodes[delivery_location[2 * n - 1], delivery_location[2 * n], t] = nodes[delivery_location[2 * n - 1], delivery_location[2 * n], t + 1] = 1
	then 0
	else ((sum{k in 1..time} nodes[delivery_location[2 * n - 1], delivery_location[2 * n], k] * flag[k]) - delivery_demand[n])
	=
	0;*/
	
# Constraint 9 - Demand Satisfaction Delivery Location
subject to Demand_Delivery_Location{n in 1..number_of_delivery_location}:
	sum{k in 2..time} nodes[delivery_location[2 * n - 1], delivery_location[2 * n], k] * flag[k] * (1 - flag[k - 1]) = delivery_demand[n];

# Constraint 10 - Should not stay in Warehouse for more than 1 Time Instant
#subject to Move_From_Warehouse{t in 1..time-1}:
#	if nodes[warehouse_location[1], warehouse_location[2], t] = 1
#	then nodes[warehouse_location[1], warehouse_location[2], t + 1] = 0;

# Constraint 11 - Stay at final Delivery Location
#subject to Stay_at_Final_Delivery_Location{i in 2..grid_size-1, j in 2..grid_size-1, t in 1..time-1, n in 1..number_of_delivery_location}:
#	if (sum{k in 2..time} nodes[delivery_location[2 * n - 1], delivery_location[2 * n], k] * flag[k] * (1 - flag[k - 1]) = delivery_demand[n])
#	then nodes[i, j, t] - nodes[i, j, t + 1] = 0;
