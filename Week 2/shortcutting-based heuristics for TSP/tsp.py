from collections import defaultdict

import numpy as np
from heapdict import heapdict
from scipy.spatial.distance import euclidean
from sklearn.neighbors import KDTree


class TSP(object):
    def __init__(self):
        self.n, self.data = self.read_data()
        self.distances = self.adj_matrix()
        self.nn = KDTree(self.data, metric='euclidean').query(self.data, k=self.n, return_distance=False)

    def read_data(self):
        with open('../data/tsp_100', 'rb') as f:
            n = int(f.readline())
            data = np.asarray([[float(x) for x in row.split()] for row in f.readlines()])
            return n, data

    def adj_matrix(self):
        adjacency_matrix = np.zeros((self.n, self.n))
        for i, node in enumerate(self.data):
            for j, neighbor in enumerate(self.data[i:]):
                adjacency_matrix[i, i + j] = adjacency_matrix[i + j, i] = euclidean(node, neighbor)
        return adjacency_matrix

    def prim(self):
        # Save the MST as adjacency list
        mst = defaultdict(list)
        # Define start node
        visited = np.zeros(self.n, dtype=bool)
        visited[0] = True
        # Initialize the heap of edges distance
        heap = heapdict()
        for node in range(1, self.n):
            heap[node] = self.distances[0, node]
        # Start iterating
        while not all(visited):
            # Grab the closest node
            new_node, distance = heap.popitem()
            # Update the MST
            for neighbor in range(self.n):
                if (neighbor != new_node) and (self.distances[new_node, neighbor] == distance):
                    mst[neighbor].append(new_node)
                    mst[new_node].append(neighbor)
                    break
            visited[new_node] = True
            # Update the distances
            for not_yet_visited in heap:
                if heap[not_yet_visited] > self.distances[new_node, not_yet_visited]:
                    heap[not_yet_visited] = self.distances[new_node, not_yet_visited]

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
        path = 0
        for index in range(self.n - 1):
            path += self.distances[tsp_path[index], tsp_path[index + 1]]
        path += self.distances[start_node, tsp_path[self.n - 1]]

        return path


def main():
    tsp = TSP()
    best_path_length = np.inf
    worst_path_length = 0
    for node in range(tsp.n):
        path_length = tsp.shortcut_dfs(node)
        if path_length < best_path_length:
            best_path_length = path_length
        if path_length > worst_path_length:
            worst_path_length = path_length
    print("Best path length: {}\nWorst path length: {}".format(best_path_length, worst_path_length))
    # Yes! The results depend on the starting node for DFS!

if __name__ == '__main__':
    main()
