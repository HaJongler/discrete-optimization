import heapq
from copy import deepcopy
from sys import stdin

import numpy as np


class Puzzle(object):
    def __init__(self):
        self.neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.solution = np.array(range(1, 17)).reshape((4, 4))
        self.solution[3, 3] = 0

    def _get_empty_cell_index(self, state):
        for i in range(4):
            for j in range(4):
                if state[i][j] == 0:
                    return (i, j)

    def _get_manhattan(self, state):
        score = 0
        for i in range(4):
            for j in range(4):
                num = state[i][j]
                if num == 0: continue
                x, y = int(np.floor(num / 4)), (num - 1) % 4
                score += np.abs(x - i) + np.abs(y - j)
        return score

    def _get_next_state(self, state):
        empty_i, empty_j = self._get_empty_cell_index(state)
        states = []
        for neighbor in self.neighbors:
            neighbor_i = empty_i + neighbor[0]
            neighbor_j = empty_j + neighbor[1]
            if (0 <= neighbor_i < 4) and (0 <= neighbor_j < 4):
                next_state = deepcopy(state)
                next_state[empty_i][empty_j], next_state[neighbor_i][neighbor_j] = next_state[neighbor_i][neighbor_j], \
                                                                                   next_state[empty_i][empty_j]
                score = self._get_manhattan(next_state)
                states.append((next_state, score))
        return states

    def solve(self, puzzle):
        # Keep track of visited states
        seen = [puzzle]
        # Initialize heap of states
        states_heap = [(self._get_manhattan(puzzle), puzzle)]
        while states_heap:
            steps_plus_score, state = heapq.heappop(states_heap)
            steps = steps_plus_score - self._get_manhattan(state)

            if np.array_equal(np.array(state), self.solution):
                return steps

            for (next_state, next_score) in self._get_next_state(state):
                if next_state not in seen:
                    seen.append(next_state)
                    heapq.heappush(states_heap, (steps + 1 + next_score, next_state))


def read_data():
    return [[int(x) for x in line.split()] for line in stdin.readlines()]


def main():
    puzzle = read_data()
    steps = Puzzle().solve(puzzle)
    print(steps)


if __name__ == '__main__':
    main()
