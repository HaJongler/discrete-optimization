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

    def mwpm(self):
        # Get the list of all odd degree vertices
        odd_degrees = [node for node in self.graph if len(self.graph[node]) % 2 != 0]
        # Find MWPM using greedy approach
        # Initialize heap of edges
        edges_heap = heapdict()
        for vertex_index, vertex in enumerate(odd_degrees):
            for neighbor_index, neighbor in enumerate(odd_degrees):
                if neighbor_index > vertex_index:
                    edges_heap[(vertex, neighbor)] = self.distances[vertex, neighbor]
        # Iterate and pick the shortest available edge
        visited = np.zeros(self.n, dtype=bool)
        mwpm = []
        while edges_heap:
            edge, distance = edges_heap.popitem()
            if visited[edge[0]] or visited[edge[1]]:
                continue
            else:
                mwpm.append(edge)
                visited[edge[0]] = visited[edge[1]] = True

        return mwpm

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def remove_edge(self, u, v):
        for index, key in enumerate(self.graph[u]):
            if key == v:
                self.graph[u].pop(index)
                break
        for index, key in enumerate(self.graph[v]):
            if key == u:
                self.graph[v].pop(index)
                break

    def DFSCount(self, v, visited):
        count = 1
        visited[v] = True
        for i in self.graph[v]:
            if visited[i] == False:
                count = count + self.DFSCount(i, visited)
        return count

    def is_valid_next_edge(self, u, v):
        # The edge u-v is valid in one of the following two cases:
        #  1) If v is the only adjacent vertex of u
        if len(self.graph[u]) == 1:
            return True
        else:
            # count of vertices reachable from u
            visited = np.zeros(self.n, dtype=bool)
            count1 = self.DFSCount(u, visited)
            self.remove_edge(u, v)
            visited = np.zeros(self.n, dtype=bool)
            count2 = self.DFSCount(u, visited)

            # 2.c) Add the edge back to the graph
            self.add_edge(u, v)

            # 2.d) If count1 is greater, then edge (u, v) is a bridge
            return False if count1 > count2 else True

    def get_euler(self, u):
        self.euler_path.append(u)
        # Recur for all the vertices adjacent to this vertex
        for v in self.graph[u]:
            # If edge u-v is not removed and it's a a valid next edge
            if self.is_valid_next_edge(u, v):
                self.remove_edge(u, v)
                self.get_euler(v)

    def christophides(self):
        # Find MST
        self.graph = self.prim()
        # get MWPM
        mwpm = self.mwpm()
        # Merge the graph
        for edge in mwpm:
            self.add_edge(*edge)
        # Find euler path
        self.euler_path = []
        self.get_euler(0)
        # Remove dups
        tsp_path = []
        for item in self.euler_path:
            if item not in tsp_path:
                tsp_path.append(item)
        # Calculate length
        path = 0
        for index in range(self.n - 1):
            path += self.distances[tsp_path[index], tsp_path[index + 1]]
        path += self.distances[0, tsp_path[self.n - 1]]

        return path


def main():
    tsp = TSP()
    print(tsp.christophides())
    # Yes, comparing to the previous algorithm, Christophides performs better!
    # Not by a lot though, the changes are between 1% ~ 10% from the best run of shortcutting.
    # Regarding the pure greedy heuristics, it is better than NN and ~equal to NI or MF,
    # sometimes giving better results and sometimes worse.


if __name__ == '__main__':
    main()
