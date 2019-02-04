import numpy as np
from scipy.spatial.distance import euclidean
from sklearn.neighbors import KDTree

class TSP(object):
    def __init__(self):
        self.n, self.data = self.read_graph()
        self.visited = np.zeros(self.n, dtype=bool)
        self.nn = KDTree(self.data, metric='euclidean').query(self.data, k=self.n, return_distance=False)

    def read_graph(self):
        with open('tsp_9432', 'rb') as f:
            n = int(f.readline())
            data = np.asarray([map(float, row.split()) for row in f.readlines()])
            return n, data


    def nearest_neighbour(self, start_index):
        self.visited = np.zeros(self.n, dtype=bool)
        # Keep track of total circuit size
        circuit = 0
        # Start from start_node
        node = start_index
        self.visited[start_index] = True
        # While we haven't visited all nodes
        while not all(self.visited):
            distance = 0
            neighbor = None
            for neighbor in self.nn[node][1:]:
                if not self.visited[neighbor]:
                    distance = euclidean(self.data[node], self.data[neighbor])
                    break
            circuit += distance
            node = neighbor
            self.visited[node] = True

        # Add the last step
        circuit += euclidean(self.data[node], start_index)
        return circuit


    def nearest_insertion(self):
        pass

    def multi_fragment(self):
        pass

    def prim(self):
        pass

def run_nn():
    tsp = TSP()
    mx = 0
    mn = np.inf
    for i in range(9432):
        new = tsp.nearest_neighbour(i)
        if new < mn:
            mn = new
        if new > mx:
            mx = new
    print "Max circuit found: {}\nMin circuit found: {}".format(mx, mn)
    # Max circuit found: 20683.2572485
    # Min circuit found: 18268.7340812
    # The difference is more than 10% of MAX result!
    # The result of NN search depends HEAVILY on the start vertex


def main():
    run_nn()

if __name__ == '__main__':
    main()
