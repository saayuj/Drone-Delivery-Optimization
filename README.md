# Introduction
This repository contains the work performed during the final year R & D Project at the Indian Institute of Technology Bombay. I worked with my peer Purushotham Mani under the supervision of Prof Avinash Bhardwaj, Dept. of Industrial Engineering and Operations Research, IITB.

# Guide
- For a detailed description, methodology, and results of the project, the manuscript [Drone Delivery Optimization.pdf](https://github.com/saayuj/Drone-Delivery-Optimization/blob/main/Drone%20Delivery%20Optimization.pdf) can be viewed. The manuscript has also been uploaded on arXiv. [link](https://arxiv.org/abs/2311.17375)
- The project proposal and final poster for the presentation have also been added.
- A guide to the various folders:
  1. The main optimization codes written to solve the various cases, along with the helper codes, can be found in [python_codes](https://github.com/saayuj/Drone-Delivery-Optimization/tree/main/python_codes).
  2. The optimization log files for each case can be found in [log_files](https://github.com/saayuj/Drone-Delivery-Optimization/tree/main/log_files).
  3. The results for all the cases can be found in [images_GIFs](https://github.com/saayuj/Drone-Delivery-Optimization/tree/main/images_GIFs).

# Results
For clarity and ease of interpretation, a color-coded grid system has been implemented, using the following key:
- Black: Location of obstacles not traversable by the drone (predetermined for a problem setting)
- Blue: Location of battery charging stations (predetermined for a problem setting)
- Red: Initial and final points of the drone (predetermined for a problem setting)
- Purple: Location of battery charging stations that are visited by the drone (given by the model)
- Green: Grid points that are visited by the drone (given by the model)
- White: Other grid points

## Optimizing the Location of Battery Charging Stations
- In this problem, the obstacles are initialized randomly, and the model gives the minimum number of battery charging stations and their locations required for servicing the entire grid.
- This means that each and every grid cell that does not contain an obstacle has at least one battery charging station within a distance of 2√2 (a variable parameter). This ensures that each and every node is reachable from a battery charging station.
- Secondly, all the battery charging stations are themselves connected to each other, i.e. there exists a path from each battery charging station to every other battery charging station. This directly implies that a path exists between each free grid cell and every other free grid cell.
- The images below show the model's output for two cases:

&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <img src="https://github.com/saayuj/Drone-Delivery-Optimization/blob/main/images_GIFs/optimal_bcs_3.png" width="300" height="300"> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <img src="https://github.com/saayuj/Drone-Delivery-Optimization/blob/main/images_GIFs/optimal_bcs_4.png" width="300" height="300"> 

## Shortest Path Problem
- In this problem, the locations of the battery charging stations, obstacles, and the initial and final points are randomly chosen and act as inputs to the model. The initial and final points can be considered to be the warehouse and delivery locations in the real-world scenario.
- The model gives the shortest feasible connected path, keeping in mind the battery constraints of the drones.
- The images below show the model's output for two cases:

&nbsp; &nbsp; &nbsp; &nbsp; <img src="https://github.com/saayuj/Drone-Delivery-Optimization/blob/main/images_GIFs/shortest_path_1.png" width="310" height="300"> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <img src="https://github.com/saayuj/Drone-Delivery-Optimization/blob/main/images_GIFs/shortest_path_2.png" width="310" height="300"> 

## Shortest Path Problem - 3D
- This problem is the same as the Shortest Path Problem described above, just extended to three-dimensional space. The color-coding is same as before.
- The image below shows the model's output:

![](https://github.com/saayuj/Drone-Delivery-Optimization/blob/main/images_GIFs/3d_shortest_path.png)

## Optimal Scheduling for Drone Delivery
- This problem takes as input the warehouse locations, the delivery locations, the number of drones, and the demand of each delivery location, and outputs the position of the drones at each time instant.
- The updated key for the color-coded grid system is as follows:
  1. Red: Warehouse locations for the drones (predetermined for a problem setting)
  2. Blue: Delivery locations (predetermined for a problem setting)
  3. Purple: Location of drone 1 (given by the model)
  4. Green: Location of drone 2 (given by the model)
  5. White: Other grid points
- The GIFs below show the model's output for two cases:

<img src="https://github.com/saayuj/Drone-Delivery-Optimization/blob/main/images_GIFs/optimal_scheduling_3del.gif" width="400" height="300">  <img src="https://github.com/saayuj/Drone-Delivery-Optimization/blob/main/images_GIFs/optimal_scheduling_3del_2.gif" width="400" height="300"> 
