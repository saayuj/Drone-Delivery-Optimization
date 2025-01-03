import heapq
from collections import defaultdict



class DistanceBetweenNodes:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, node_1, node_2, distance_between_nodes_1_and_2):
        self.graph[node_1].append((node_2, distance_between_nodes_1_and_2))
        self.graph[node_2].append((node_1, distance_between_nodes_1_and_2))

    def dijkstra_distance(self, start_node, end_node):
        if start_node not in self.graph or end_node not in self.graph:
            return float('inf')  # Nodes not found in the graph

        distances = {node: float('inf') for node in self.graph}
        distances[start_node] = 0

        priority_queue = [(0, start_node)]  # Priority queue for (distance, node)

        while priority_queue:
            distance, current_node = heapq.heappop(priority_queue)

            if current_node == end_node:
                return distance  # Distance found

            if distance > distances[current_node]:
                continue  # Skip if we found a shorter path

            for neighbor, weight in self.graph[current_node]:
                new_distance = distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        return float('inf')  # No path found between start and end nodes
