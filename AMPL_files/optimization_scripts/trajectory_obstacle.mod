# Parameters
param grid_size;
param obstacles_number;
param initial_final_points{i in 1..4};
param obstacles{i in 1..(2*obstacles_number)};

# Decision Variable
var x{i in 1..grid_size, j in 1..grid_size} binary;

# Objective Function
minimize Cost:
    sum{i in 1..grid_size, j in 1..grid_size} x[i, j];

# Constraint 1 - Initial and Final Points should be 1
subject to Initial_and_Final_Points_One{i in 1..2}:
	x[initial_final_points[2 * i - 1], initial_final_points[2 * i]] = 1;

# Constraint 2 - Obstacles should be 0
subject to Obstacles_Zero{i in 1..obstacles_number}:
	x[obstacles[2 * i - 1], obstacles[2 * i]] = 0;

# Constraint 3 - Path should be Connected except Initial and Final Points
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

# Constraint 4 - Path should be Connected for Initial Point
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

# Constraint 5 - Path should be Connected for Final Point
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

# Constraint 6 - Max 2 Points in a 2x2 Square
subject to Max_Two_Points{i in 1..(grid_size - 1), j in 1..(grid_size - 1)}:
	sum{k in i..i+1, l in j..j+1} x[k, l] <= 2;
