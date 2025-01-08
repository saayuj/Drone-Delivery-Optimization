# Parameters
param grid_size;
param cost_per_hop;
param battery_swapping_stations_number;
param initial_final_points{i in 1..4};
param battery_swapping_stations{i in 1..(2*battery_swapping_stations_number)};
param battery_added{i in 1..grid_size, j in 1..grid_size};

# Decision Variable
var x{i in 1..grid_size, j in 1..grid_size} binary;
var d{i in 1..grid_size, j in 1..grid_size} binary;

# Objective Function
minimize Cost:
    sum{i in 1..grid_size, j in 1..grid_size} x[i, j];

# Constraint 1 - Initial and Final Points should be 1
subject to Initial_and_Final_Points_One{i in 1..2}:
	x[initial_final_points[2 * i - 1], initial_final_points[2 * i]] = 1;

# Constraint 2 - Path should be Connected except Initial and Final Points
subject to Path_Connected_except_Initial_and_Final_Points{i in 1..grid_size, j in 1..grid_size}:
	(if (2 <= i <= 9 && 2 <= j <= 9)
	then (sum{k in i-1..i+1, l in j-1..j+1} x[k, l])
	else if (i = 1 && 2 <= j <= 9)
	then (sum{k in i..i+1, l in j-1..j+1} x[k, l])
	else if (i = 10 && 2 <= j <= 9)
	then (sum{k in i-1..i, l in j-1..j+1} x[k, l])
	else if (2 <= i <= 9 && j = 1)
	then (sum{k in i-1..i+1, l in j..j+1} x[k, l])
	else if (2 <= i <= 9 && j = 10)
	then (sum{k in i-1..i+1, l in j-1..j} x[k, l])
	else if (i = 1 && j = 1)
	then (sum{k in i..i+1, l in j..j+1} x[k, l])
	else if (i = 1 && j = 10)
	then (sum{k in i..i+1, l in j-1..j} x[k, l])
	else if (i = 10 && j = 1)
	then (sum{k in i-1..i, l in j..j+1} x[k, l])
	else (sum{k in i-1..i, l in j-1..j} x[k, l])
	)
    >=
    (if (i != initial_final_points[1] or j != initial_final_points[2]) && 
    (i != initial_final_points[3] or j != initial_final_points[4])
    then (3 * x[i, j])
    else (0)
    );

# Constraint 3 - Path should be Connected for Initial Point
subject to Path_Connected_only_Initial_Point:
	(if (2 <= initial_final_points[1] <= 9 && 2 <= initial_final_points[2] <= 9)
	then (sum{k in initial_final_points[1]-1..initial_final_points[1]+1, l in initial_final_points[2]-1..initial_final_points[2]+1} x[k, l])
	else if (initial_final_points[1] = 1 && 2 <= initial_final_points[2] <= 9)
	then (sum{k in initial_final_points[1]..initial_final_points[1]+1, l in initial_final_points[2]-1..initial_final_points[2]+1} x[k, l])
	else if (initial_final_points[1] = 10 && 2 <= initial_final_points[2] <= 9)
	then (sum{k in initial_final_points[1]-1..initial_final_points[1], l in initial_final_points[2]-1..initial_final_points[2]+1} x[k, l])
	else if (2 <= initial_final_points[1] <= 9 && initial_final_points[2] = 1)
	then (sum{k in initial_final_points[1]-1..initial_final_points[1]+1, l in initial_final_points[2]..initial_final_points[2]+1} x[k, l])
	else if (2 <= initial_final_points[1] <= 9 && initial_final_points[2] = 10)
	then (sum{k in initial_final_points[1]-1..initial_final_points[1]+1, l in initial_final_points[2]-1..initial_final_points[2]} x[k, l])
	else if (initial_final_points[1] = 1 && initial_final_points[2] = 1)
	then (sum{k in initial_final_points[1]..initial_final_points[1]+1, l in initial_final_points[2]..initial_final_points[2]+1} x[k, l])
	else if (initial_final_points[1] = 1 && initial_final_points[2] = 10)
	then (sum{k in initial_final_points[1]..initial_final_points[1]+1, l in initial_final_points[2]-1..initial_final_points[2]} x[k, l])
	else if (initial_final_points[1] = 10 && initial_final_points[2] = 1)
	then (sum{k in initial_final_points[1]-1..initial_final_points[1], l in initial_final_points[2]..initial_final_points[2]+1} x[k, l])
	else if (initial_final_points[1] = 10 && initial_final_points[2] = 10)
	then (sum{k in initial_final_points[1]-1..initial_final_points[1], l in initial_final_points[2]-1..initial_final_points[2]} x[k, l])
	)
    =
    2;

# Constraint 4 - Path should be Connected for Final Point
subject to Path_Connected_only_Final_Point:
	(if (2 <= initial_final_points[3] <= 9 && 2 <= initial_final_points[4] <= 9)
	then (sum{k in initial_final_points[3]-1..initial_final_points[3]+1, l in initial_final_points[4]-1..initial_final_points[4]+1} x[k, l])
	else if (initial_final_points[3] = 1 && 2 <= initial_final_points[4] <= 9)
	then (sum{k in initial_final_points[3]..initial_final_points[3]+1, l in initial_final_points[4]-1..initial_final_points[4]+1} x[k, l])
	else if (initial_final_points[3] = 10 && 2 <= initial_final_points[4] <= 9)
	then (sum{k in initial_final_points[3]-1..initial_final_points[3], l in initial_final_points[4]-1..initial_final_points[4]+1} x[k, l])
	else if (2 <= initial_final_points[3] <= 9 && initial_final_points[4] = 1)
	then (sum{k in initial_final_points[3]-1..initial_final_points[3]+1, l in initial_final_points[4]..initial_final_points[4]+1} x[k, l])
	else if (2 <= initial_final_points[3] <= 9 && initial_final_points[4] = 10)
	then (sum{k in initial_final_points[3]-1..initial_final_points[3]+1, l in initial_final_points[4]-1..initial_final_points[4]} x[k, l])
	else if (initial_final_points[3] = 1 && initial_final_points[4] = 1)
	then (sum{k in initial_final_points[3]..initial_final_points[3]+1, l in initial_final_points[4]..initial_final_points[4]+1} x[k, l])
	else if (initial_final_points[3] = 1 && initial_final_points[4] = 10)
	then (sum{k in initial_final_points[3]..initial_final_points[3]+1, l in initial_final_points[4]-1..initial_final_points[4]} x[k, l])
	else if (initial_final_points[3] = 10 && initial_final_points[4] = 1)
	then (sum{k in initial_final_points[3]-1..initial_final_points[3], l in initial_final_points[4]..initial_final_points[4]+1} x[k, l])
	else if (initial_final_points[3] = 10 && initial_final_points[4] = 10)
	then (sum{k in initial_final_points[3]-1..initial_final_points[3], l in initial_final_points[4]-1..initial_final_points[4]} x[k, l])
	)
    =
    2;

# Constraint 5 - Max 2 Points in a 2x2 Square if BSS not present, otherwise 3
subject to Max_Two_or_Three_Points{i in 1..(grid_size - 1), j in 1..(grid_size - 1)}:
	sum{k in i..i+1, l in j..j+1} x[k, l] 
	<= 
	(if (i <= battery_swapping_stations[1] <= i+1 && j <= battery_swapping_stations[2] <= j+1) or 
	(i <= battery_swapping_stations[3] <= i+1 && j <= battery_swapping_stations[4] <= j+1) or 
	(i <= battery_swapping_stations[5] <= i+1 && j <= battery_swapping_stations[6] <= j+1)
	then (3)
	else (2)
	);

# Constraint 6 - Battery Level should be Positive at each Hop
subject to Battery_Level_Positive{i in 1..grid_size, j in 1..grid_size}:
	(if (3 <= i <= 8 && 3 <= j <= 8)
	then (sum{k in i-2..i+2, l in j-2..j+2} d[k, l])
	else if (i = 2 && 3 <= j <= 8)
	then (sum{k in i-1..i+2, l in j-2..j+2} d[k, l])
	else if (i = 1 && 3 <= j <= 8)
	then (sum{k in i..i+2, l in j-2..j+2} d[k, l])
	else if (i = 9 && 3 <= j <= 8)
	then (sum{k in i-2..i+1, l in j-2..j+2} d[k, l])
	else if (i = 10 && 3 <= j <= 8)
	then (sum{k in i-2..i, l in j-2..j+2} d[k, l])
	else if (3 <= i <= 8 && j = 2)
	then (sum{k in i-2..i+2, l in j-1..j+2} d[k, l])
	else if (3 <= i <= 8 && j = 1)
	then (sum{k in i-2..i+2, l in j..j+2} d[k, l])
	else if (3 <= i <= 8 && j = 9)
	then (sum{k in i-2..i+2, l in j-2..j+1} d[k, l])
	else if (3 <= i <= 8 && j = 10)
	then (sum{k in i-2..i+2, l in j-2..j} d[k, l])
	else if (i = 1 && j = 1)
	then (sum{k in i..i+2, l in j..j+2} d[k, l])
	else if (i = 1 && j = 2)
	then (sum{k in i..i+2, l in j-1..j+2} d[k, l])
	else if (i = 2 && j = 1)
	then (sum{k in i-1..i+2, l in j..j+2} d[k, l])
	else if (i = 2 && j = 2)
	then (sum{k in i-1..i+2, l in j-1..j+2} d[k, l])
	else if (i = 1 && j = 9)
	then (sum{k in i..i+2, l in j-2..j+1} d[k, l])
	else if (i = 1 && j = 10)
	then (sum{k in i..i+2, l in j-2..j} d[k, l])
	else if (i = 2 && j = 9)
	then (sum{k in i-1..i+2, l in j-2..j+1} d[k, l])
	else if (i = 2 && j = 10)
	then (sum{k in i-1..i+2, l in j-2..j} d[k, l])
	else if (i = 9 && j = 1)
	then (sum{k in i-2..i+1, l in j..j+2} d[k, l])
	else if (i = 9 && j = 2)
	then (sum{k in i-2..i, l in j-1..j+2} d[k, l])
	else if (i = 10 && j = 1)
	then (sum{k in i-2..i, l in j..j+2} d[k, l])
	else if (i = 10 && j = 2)
	then (sum{k in i-2..i, l in j-1..j+2} d[k, l])
	else if (i = 9 && j = 9)
	then (sum{k in i-2..i+1, l in j-2..j+1} d[k, l])
	else if (i = 9 && j = 10)
	then (sum{k in i-2..i+1, l in j-2..j} d[k, l])
	else if (i = 10 && j = 9)
	then (sum{k in i-2..i, l in j-2..j+1} d[k, l])
	else if (i = 10 && j = 10)
	then (sum{k in i-2..i, l in j-2..j} d[k, l])
	)
	>=
	(if (i = initial_final_points[1] && j = initial_final_points[2]) or 
    (i = initial_final_points[3] && j = initial_final_points[4])
    then (2 * d[i, j])
    else (3 * d[i, j])
    );

# Constraint 7 - Define new Matrix d_ij which is intersection of Visited Points & BSS
subject to Form_Matrix_D{i in 1..grid_size, j in 1..grid_size}:
	d[i, j] = x[i, j] * battery_added[i, j] / 10;

# Constraint 8 - Minimum BSS that must be Visited
#subject to Minimum_BSS_Visited:
#	sum {i in 1..grid_size, j in 1..grid_size} d[i, j] >=
#	floor(max(abs(initial_final_points[1] - initial_final_points[3]), abs(initial_final_points[2] - initial_final_points[4])) / 2 - 0.5) + 2;
