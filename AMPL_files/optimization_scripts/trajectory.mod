# Parameters
param grid_size;
param initial_final_points{i in 1..4};
param distance_matrix{i in 1..grid_size, j in 1..grid_size, k in 1..grid_size, l in 1..grid_size};

# Decision Variable
var x{i in 1..grid_size, j in 1..grid_size} binary;

# Objective Function
minimize Cost:
#    sum{i in 1..grid_size, j in 1..grid_size} x[i, j];
	sum{i in 1..grid_size, j in 1..grid_size, k in 1..grid_size, l in 1..grid_size} distance_matrix[i, j, k, l] * x[i, j] * x[k, l] / 2;

# Constraint 1 - Initial and Final Points should be 1
subject to Initial_and_Final_Points_One{i in 1..2}:
	x[initial_final_points[2 * i - 1], initial_final_points[2 * i]] = 1;

# Constraint 2 - Path should be Connected except Initial and Final Points
subject to Path_Connected_except_Initial_and_Final_Points{i in 1..grid_size, j in 1..grid_size}:
	(if (2 <= i <= grid_size-1 && 2 <= j <= grid_size-1)
	then (sum{k in i-1..i+1, l in j-1..j+1} x[k, l])
	else if (i = 1 && 2 <= j <= grid_size-1)
	then (sum{k in i..i+1, l in j-1..j+1} x[k, l])
	else if (i = grid_size && 2 <= j <= grid_size-1)
	then (sum{k in i-1..i, l in j-1..j+1} x[k, l])
	else if (2 <= i <= grid_size-1 && j = 1)
	then (sum{k in i-1..i+1, l in j..j+1} x[k, l])
	else if (2 <= i <= grid_size-1 && j = grid_size)
	then (sum{k in i-1..i+1, l in j-1..j} x[k, l])
	else if (i = 1 && j = 1)
	then (sum{k in i..i+1, l in j..j+1} x[k, l])
	else if (i = 1 && j = grid_size)
	then (sum{k in i..i+1, l in j-1..j} x[k, l])
	else if (i = grid_size && j = 1)
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
	(if (2 <= initial_final_points[1] <= grid_size-1 && 2 <= initial_final_points[2] <= grid_size-1)
	then (sum{k in initial_final_points[1]-1..initial_final_points[1]+1, l in initial_final_points[2]-1..initial_final_points[2]+1} x[k, l])
	else if (initial_final_points[1] = 1 && 2 <= initial_final_points[2] <= grid_size-1)
	then (sum{k in initial_final_points[1]..initial_final_points[1]+1, l in initial_final_points[2]-1..initial_final_points[2]+1} x[k, l])
	else if (initial_final_points[1] = grid_size && 2 <= initial_final_points[2] <= grid_size-1)
	then (sum{k in initial_final_points[1]-1..initial_final_points[1], l in initial_final_points[2]-1..initial_final_points[2]+1} x[k, l])
	else if (2 <= initial_final_points[1] <= grid_size-1 && initial_final_points[2] = 1)
	then (sum{k in initial_final_points[1]-1..initial_final_points[1]+1, l in initial_final_points[2]..initial_final_points[2]+1} x[k, l])
	else if (2 <= initial_final_points[1] <= grid_size-1 && initial_final_points[2] = grid_size)
	then (sum{k in initial_final_points[1]-1..initial_final_points[1]+1, l in initial_final_points[2]-1..initial_final_points[2]} x[k, l])
	else if (initial_final_points[1] = 1 && initial_final_points[2] = 1)
	then (sum{k in initial_final_points[1]..initial_final_points[1]+1, l in initial_final_points[2]..initial_final_points[2]+1} x[k, l])
	else if (initial_final_points[1] = 1 && initial_final_points[2] = grid_size)
	then (sum{k in initial_final_points[1]..initial_final_points[1]+1, l in initial_final_points[2]-1..initial_final_points[2]} x[k, l])
	else if (initial_final_points[1] = grid_size && initial_final_points[2] = 1)
	then (sum{k in initial_final_points[1]-1..initial_final_points[1], l in initial_final_points[2]..initial_final_points[2]+1} x[k, l])
	else if (initial_final_points[1] = grid_size && initial_final_points[2] = grid_size)
	then (sum{k in initial_final_points[1]-1..initial_final_points[1], l in initial_final_points[2]-1..initial_final_points[2]} x[k, l])
	)
    =
    2;

# Constraint 4 - Path should be Connected for Final Point
subject to Path_Connected_only_Final_Point:
	(if (2 <= initial_final_points[3] <= grid_size-1 && 2 <= initial_final_points[4] <= grid_size-1)
	then (sum{k in initial_final_points[3]-1..initial_final_points[3]+1, l in initial_final_points[4]-1..initial_final_points[4]+1} x[k, l])
	else if (initial_final_points[3] = 1 && 2 <= initial_final_points[4] <= grid_size-1)
	then (sum{k in initial_final_points[3]..initial_final_points[3]+1, l in initial_final_points[4]-1..initial_final_points[4]+1} x[k, l])
	else if (initial_final_points[3] = grid_size && 2 <= initial_final_points[4] <= grid_size-1)
	then (sum{k in initial_final_points[3]-1..initial_final_points[3], l in initial_final_points[4]-1..initial_final_points[4]+1} x[k, l])
	else if (2 <= initial_final_points[3] <= grid_size-1 && initial_final_points[4] = 1)
	then (sum{k in initial_final_points[3]-1..initial_final_points[3]+1, l in initial_final_points[4]..initial_final_points[4]+1} x[k, l])
	else if (2 <= initial_final_points[3] <= grid_size-1 && initial_final_points[4] = grid_size)
	then (sum{k in initial_final_points[3]-1..initial_final_points[3]+1, l in initial_final_points[4]-1..initial_final_points[4]} x[k, l])
	else if (initial_final_points[3] = 1 && initial_final_points[4] = 1)
	then (sum{k in initial_final_points[3]..initial_final_points[3]+1, l in initial_final_points[4]..initial_final_points[4]+1} x[k, l])
	else if (initial_final_points[3] = 1 && initial_final_points[4] = grid_size)
	then (sum{k in initial_final_points[3]..initial_final_points[3]+1, l in initial_final_points[4]-1..initial_final_points[4]} x[k, l])
	else if (initial_final_points[3] = grid_size && initial_final_points[4] = 1)
	then (sum{k in initial_final_points[3]-1..initial_final_points[3], l in initial_final_points[4]..initial_final_points[4]+1} x[k, l])
	else if (initial_final_points[3] = grid_size && initial_final_points[4] = grid_size)
	then (sum{k in initial_final_points[3]-1..initial_final_points[3], l in initial_final_points[4]-1..initial_final_points[4]} x[k, l])
	)
    =
    2;

# Constraint 5 - Max 2 Points in a 2x2 Square
subject to Max_Two_Points{i in 1..(grid_size - 1), j in 1..(grid_size - 1)}:
	sum{k in i..i+1, l in j..j+1} x[k, l] <= 2;
