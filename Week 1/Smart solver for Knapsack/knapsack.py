import pymzn, datetime

def main():

    k4 = pymzn.dzn2dict('knapsack-4.dzn')
    k19 = pymzn.dzn2dict('knapsack-19.dzn')
    k60 = pymzn.dzn2dict('knapsack-60.dzn')
    k100 = pymzn.dzn2dict('knapsack-100.dzn')
    k400 = pymzn.dzn2dict('knapsack-400.dzn')
    k10k = pymzn.dzn2dict('knapsack-10000.dzn')
    k = k10k

    class DFS(object):
        def __init__(self, ws, vs, mw):
            self.data = sorted(zip(ws, vs), reverse=True,
                               key=lambda w_v: float(w_v[1]) / w_v[0])
            self.max_weight = float(mw)
            self.lowerbound = 0
            self.acc_val = 0
            self.acc_weight = 0

        def calculate_upperbound(self, index, max_weight):
            current_value = 0
            current_weight = 0
            for item in self.data[index:]:
                if current_weight + item[0] <= max_weight:
                    current_weight += item[0]
                    current_value += item[1]
                else:
                    current_value += item[1] * (max_weight - current_weight) / item[0]
                    break
            return current_value

        def dfs(self):
            # Initialize a stack of tuples <index, include_in_knapsack>
            stack = [(0, False), (0, True)]
            # Start DFSing
            while stack:
                node, include_in_knapsack = stack.pop()
                if include_in_knapsack:
                    # We add the value to our accumulated value and the weight to accumulated weight
                    self.acc_val += self.data[node][1]
                    self.acc_weight += self.data[node][0]
                    # If it's not too much weight we continue DFSing and update the lowerbound.
                    if self.acc_weight <= self.max_weight:
                        # We then check if the new accumulated value is bigger than what we ever saw
                        if self.lowerbound < self.acc_val:
                            self.lowerbound = self.acc_val  # If yes, we update
                        # And now if we are not at the end of the list, we DFS to the next node
                        if (node + 1 < len(self.data)) \
                                and (self.acc_val +
                                     self.calculate_upperbound(node + 1, self.max_weight - self.acc_weight) >= self.lowerbound):
                            stack.append((node + 1, False))
                            stack.append((node + 1, True))

                else:
                    # We remove the node impact on the parameters
                    self.acc_val -= self.data[node][1]
                    self.acc_weight -= self.data[node][0]
                    # And now if we are not at the end of the list, we DFS to the next node
                    if (node + 1 < len(self.data)) and (self.acc_val + self.calculate_upperbound(node + 1, self.max_weight - self.acc_weight) >= self.lowerbound):
                        stack.append((node + 1, False))
                        stack.append((node + 1, True))

    d = DFS(k['weight'], k['value'], k['weight_limit'])
    print(datetime.datetime.now())
    d.dfs()
    print(d.lowerbound)
    print(datetime.datetime.now())

if __name__ == '__main__':
    main()