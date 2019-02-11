import logging
from collections import defaultdict

import numpy as np
from heapdict import heapdict
from scipy.spatial.distance import euclidean
from tqdm import tqdm

DEFAULT_LANDMARKS_QUANTITY = 0


class AStar(object):
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

    def _dijkstra(self, start_node):
        sssp = dict()
        # Initialize vertices heapdict<node: distance>
        vertices_heap = heapdict({start_node: 0})
        visited = defaultdict(bool)
        # Start pulling from the heap
        while vertices_heap:
            node, distance = vertices_heap.popitem()
            visited[node] = True
            # Once a node has been pulled, the distance is final
            sssp[node] = distance
            # Update the heap
            for neighbor in self.edges[node]:
                if visited[neighbor]: continue
                # If the distance in the heap is smaller then the distance to the freshly pulled node, continue
                if vertices_heap.get(neighbor, np.inf) < distance + self.edges[node][neighbor]:
                    continue
                # Otherwise, update the data in the heap
                vertices_heap[neighbor] = distance + self.edges[node][neighbor]

        return sssp

    def _search(self, source, dest, potential_function):
        logging.info("Searching for shortest path")
        visited = defaultdict(bool)
        # Initialize vertices heapdict<node: distance from source + euclidean to dest>
        vertices_heap = heapdict({source: potential_function(source)})
        # Start pulling from the heap
        while vertices_heap:
            node, distance = vertices_heap.popitem()
            visited[node] = True
            # Remove the euclidean part to get accurate distance
            distance -= potential_function(node)
            # Check if we reached our dest
            if node == dest:
                logging.info("Found shortest path of length {}".format(distance))
                break
            # Update the heap
            for neighbor in self.edges[node]:
                if visited[neighbor]: continue
                # If the distance in the heap is smaller then the distance to the freshly pulled node, continue
                if vertices_heap.get(neighbor, np.inf) < distance + self.edges[node][neighbor] + potential_function(neighbor):
                    continue
                # Otherwise, update the data in the heap
                vertices_heap[neighbor] = distance + self.edges[node][neighbor] + potential_function(neighbor)

    def _get_landmarks(self, quantity, method):
        logging.info("Finding landmarks")
        if method == 'random':
            return np.random.randint(1, len(self.vertices) + 1, quantity + 2)
        elif method == 'planar':
            pass
        else:
            pass

    def _get_best_landmark(self, landmarks, source, dest):
        logging.info("Calculating best bound")
        best_bound = -np.inf
        best_sssp = None
        sssps = [self._dijkstra(landmark) for landmark in tqdm(landmarks) if landmark not in (source, dest)]
        for sssp in sssps:
            if sssp[dest] - sssp[source] > best_bound:
                best_bound = sssp[dest] - sssp[source]
                best_sssp = sssp
        return best_sssp

    def search(self, source, dest):
        logging.info("Running A* search")
        potential_function = lambda u: euclidean(self.vertices[u], self.vertices[dest])
        self._search(source, dest, potential_function)

    def alt(self, source, dest, method, landmarks_quantity=DEFAULT_LANDMARKS_QUANTITY):
        logging.info("Running ALT with {q} {m} landmarks".format(q=landmarks_quantity, m=method))
        landmarks = self._get_landmarks(landmarks_quantity, method)
        best_sssp = self._get_best_landmark(landmarks, source, dest)
        potential_function = lambda u: best_sssp[dest] - best_sssp[u]
        self._search(source, dest, potential_function)


def read_vertices():
    logging.info("Reading data: vertices")
    data = dict()
    with open('USA-road-d.FLA.co', 'r') as f:
        for line in f:
            line = line.split()
            if line[0] == "v":
                data[int(line[1])] = (int(line[2]), int(line[3]))
    return data


def read_edges():
    logging.info("Reading data: edges")
    data = defaultdict(dict)
    with open('USA-road-t.FLA.gr', 'r') as f:
        for line in f:
            line = line.split()
            if line[0] == 'a':
                x, y, w = [int(num) for num in line[1:]]
                data[x][y] = w
    return data


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

    vertices = read_vertices()
    edges = read_edges()

    a_star = AStar(vertices, edges)
    a_star.search(1, 1001)
    a_star.alt(1, 1001, 'random')
    a_star.alt(1, 1001, 'planar')
    a_star.alt(1, 1001, 'avoid')


if __name__ == '__main__':
    main()
