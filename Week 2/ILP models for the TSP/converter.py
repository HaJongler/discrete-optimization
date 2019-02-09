from itertools import combinations

import numpy as np
import pymzn
from scipy.spatial.distance import euclidean


def read_data(size):
    with open('../data/tsp_{}'.format(size), 'rb') as f:
        n = int(f.readline())
        data = np.asarray([[float(x) for x in row.split()] for row in f.readlines()])
        return n, data


def adj_matrix(n, data):
    adjacency_matrix = np.zeros((n, n))
    for i, node in enumerate(data):
        for j, neighbor in enumerate(data[i:]):
            adjacency_matrix[i, i + j] = adjacency_matrix[i + j, i] = euclidean(node, neighbor)
    return adjacency_matrix


def subsets(s):
    for cardinality in range(len(s) + 1):
        yield from combinations(s, cardinality)


def save_as_dzn(n, matrix):
    data = {'n': n, 'matrix': matrix,
            'subsets': [set(sub_set) for sub_set in subsets(range(1, n + 1)) if 0 < len(sub_set) < n]}
    # Unfortunately we can not iterate over subsets in MiniZinc.
    # (see: https://stackoverflow.com/questions/40367148/how-to-quantify-over-all-subsets-in-minizinc)
    # That's why I have to generate all subsets in Python. It is really memory heavy and the
    # only one that actually works is tsp_5.
    pymzn.dict2dzn(data, fout='tsp_{}.dzn'.format(n))


def main():
    for size in (5, 51, 100):
        n, data = read_data(size)
        adjacency_matrix = adj_matrix(n, data)
        save_as_dzn(n, adjacency_matrix)


if __name__ == '__main__':
    main()
