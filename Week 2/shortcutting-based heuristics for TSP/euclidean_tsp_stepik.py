import heapq
from collections import defaultdict
from sys import stdin

import numpy as np
from scipy.spatial.distance import euclidean


class TSP(object):
    def __init__(self):
        self.n, self.data = self.read_data()
        self.distances = self.adj_matrix()

    def read_data(self):
        data = dict()
        n = int(stdin.readline())
        for row in range(n):
            line = stdin.readline().split()
            p = int(line[0])
            x = float(line[1])
            y = float(line[2])
            data[p] = (x, y)
        return n, data

    def adj_matrix(self):
        nodes = list(self.data.keys())
        adjacency_matrix = defaultdict(lambda: defaultdict(int))
        for node_index in range(self.n - 1):
            for neighbor_index in range(node_index, self.n):
                node = nodes[node_index]
                neighbor = nodes[neighbor_index]
                adjacency_matrix[node][neighbor] = adjacency_matrix[neighbor][node] = \
                    euclidean(self.data[node], self.data[neighbor])
        return adjacency_matrix

    def prim(self):
        # Save the MST as adjacency list
        mst = defaultdict(list)
        # Define start node
        visited = np.zeros(self.n, dtype=bool)
        visited[0] = True
        # Initialize the heap of edges distance
        my_heap = []
        for node in range(1, self.n):
            heapq.heappush(my_heap, (self.distances[0][node], node))
        # Start iterating
        while not all(visited):
            # Grab the closest node
            distance, new_node = heapq.heappop(my_heap)
            # Update the MST
            for neighbor in range(self.n):
                if (neighbor != new_node) and (self.distances[new_node][neighbor] == distance):
                    mst[neighbor].append(new_node)
                    mst[new_node].append(neighbor)
                    break
            visited[new_node] = True
            # Update the distances
            for index, (old_distance, not_yet_visited) in enumerate(my_heap):
                if old_distance > self.distances[new_node][not_yet_visited]:
                    my_heap[index] = (self.distances[new_node][not_yet_visited], not_yet_visited)
            heapq.heapify(my_heap)

        return mst

    def shortcut_dfs(self, start_node):
        # Load MST graph
        mst = self.prim()
        # Initiate variables
        tsp_path = []
        visited = np.zeros(self.n, dtype=bool)
        stack = [start_node]
        # DFS and keep a list of new nodes
        while stack:
            node = stack.pop()
            visited[node] = True
            tsp_path.append(node)
            for neighbor in mst[node]:
                if not visited[neighbor]:
                    stack.append(neighbor)
        # Calculate final TSP path length
        tsp_path.append(tsp_path[0])
        path_length = 0
        for index in range(self.n):
            path_length += self.distances[tsp_path[index]][tsp_path[index + 1]]

        return path_length, tsp_path


def main():
    tsp = TSP()
    best_path_length = np.inf
    best_path = None
    for node in range(tsp.n):
        path_length, tsp_path = tsp.shortcut_dfs(node)
        if path_length < best_path_length:
            best_path_length = path_length
            best_path = tsp_path
    print(*map(lambda x: x + 1, best_path), sep=" ")


if __name__ == '__main__':
    main()
