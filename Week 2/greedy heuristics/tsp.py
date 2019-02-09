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

    def nearest_neighbour(self, start_index):
        visited = np.zeros(self.n, dtype=bool)
        # Keep track of total circuit size
        circuit = 0
        # Start from start_node
        node = start_index
        visited[start_index] = True
        # While we haven't visited all nodes
        while not all(visited):
            distance = 0
            neighbor = None
            for neighbor in self.nn[node][1:]:
                if not visited[neighbor]:
                    distance = euclidean(self.data[node], self.data[neighbor])
                    break
            circuit += distance
            node = neighbor
            visited[node] = True

        # Add the last step
        circuit += euclidean(self.data[node], start_index)
        return circuit

    def nearest_insertion(self):
        # Def circuit length
        circuit = 0
        # Define initially visited node
        visited = np.zeros(self.n, dtype=bool)
        visited[0] = True
        # Initialize the heap of edges distance
        heap = heapdict()
        for node in range(1, self.n):
            heap[node] = self.distances[0, node]
        # Pull first node
        node, distance = heap.popitem()
        visited[node] = True
        circuit += distance
        # Start iterating
        while not all(visited):
            new_node, distance = heap.popitem()
            node_a = node_b = None
            for neighbor in self.nn[new_node][1:]:
                if visited[neighbor] and node_a is None:
                    node_a = neighbor
                elif visited[neighbor] and node_b is None:
                    node_b = neighbor
                    break
            circuit -= self.distances[node_a, node_b]
            circuit += self.distances[node_a, new_node]
            circuit += self.distances[node_b, new_node]
            visited[new_node] = True

        return circuit

    def check_circle(self, graph, node):
        start_node = parent = node
        counter = 1
        while True:
            if len(graph[node]) <= 1:
                return 0
            for neighbor in graph[node]:
                if neighbor == parent:
                    continue
                if neighbor == start_node:
                    return counter
                parent = node
                node = neighbor
                counter += 1
                break

    def multi_fragment(self):
        circuit = 0

        edges_heap = heapdict()
        for i in range(self.n - 1):
            for j in range(i + 1, self.n):
                edges_heap[(i, j)] = self.distances[i, j]

        graph = defaultdict(list)
        while self.check_circle(graph, 0) != self.n:
            (node_a, node_b), weight = edges_heap.popitem()
            graph[node_a].append(node_b)
            graph[node_b].append(node_a)
            if (len(graph[node_a]) > 2) or (len(graph[node_b]) > 2) or (0 < self.check_circle(graph, node_a) < self.n):
                graph[node_b].pop()
                graph[node_a].pop()
            else:
                circuit += weight

        return circuit

    def prim(self):
        mst = 0
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
            # Update the values
            mst += distance
            visited[new_node] = True
            # Update the distances
            for not_yet_visited in heap:
                if heap[not_yet_visited] > self.distances[new_node, not_yet_visited]:
                    heap[not_yet_visited] = self.distances[new_node, not_yet_visited]

        return mst


def test_nn_different_start_nodes(tsp):
    mx = 0
    mn = np.inf
    for i in range(9432):
        new = tsp.nearest_neighbour(i)
        if new < mn:
            mn = new
        if new > mx:
            mx = new
    print("Max circuit found: {}\nMin circuit found: {}".format(mx, mn))
    # Max circuit found: 20683.2572485
    # Min circuit found: 18268.7340812
    # The difference is more than 10% of MAX result!
    # The result of NN search depends HEAVILY on the start vertex


def main():
    tsp = TSP()
    print(tsp.prim())
    print(tsp.nearest_neighbour(0))
    print(tsp.nearest_insertion())
    print(tsp.multi_fragment())
    # test_nn_different_start_nodes(tsp)

    ###############
    # BEST SCORES #
    ###############

    # TSP_5    : NI
    # TSP_51   : NI
    # TSP_100  : MF
    # TSP_400  : NI
    # TSP_9432 : NI?


if __name__ == '__main__':
    main()
