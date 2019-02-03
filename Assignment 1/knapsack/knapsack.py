import pymzn, datetime

def calculate_upperbound(w, v, mw):
    current_value = 0
    current_weight = 0
    data = sorted(zip(w,v), key=lambda w_v: float(w_v[1]) / w_v[0], reverse=True)
    for item in data:
        if current_weight + item[0] <= mw:
            current_weight += item[0]
            current_value += item[1]
        else:
            current_value += item[1] * (float(mw - current_weight) / item[0])
            break
        return current_value


def main():

    k4 = pymzn.dzn2dict('knapsack-4.dzn')
    k19 = pymzn.dzn2dict('knapsack-19.dzn')
    k60 = pymzn.dzn2dict('knapsack-60.dzn')
    k100 = pymzn.dzn2dict('knapsack-100.dzn')
    k400 = pymzn.dzn2dict('knapsack-400.dzn')
    k10k = pymzn.dzn2dict('knapsack-10000.dzn')
    k = k400

    class DFS(object):
        def __init__(self, ws, vs, mw):
            self.data = sorted(zip(ws, vs), reverse=True,
                               key=lambda w_v: float(w_v[1]) / w_v[0])
            self.max_weight = mw
            self.upperbound = sum(vs)
            self.lowerbound = 0
            self.acc_val = 0
            self.acc_weight = 0
            self.first_lb()

        def first_lb(self):
            weight = 0
            for item in self.data:
                if weight + item[0] <= self.max_weight:
                    weight += item[0]
                    self.lowerbound += item[1]

        def dfs(self, index):
            # Check if we even want to check this node
            if self.upperbound < self.lowerbound: return
            # Mark if used it or not
            used = False
            # If we do, then consider two cases: take it / don't take it
            for take in (False, True):
                if take:
                    # If we decide to take the item, we check if it's even possible (max_weight wise)
                    if self.acc_weight + self.data[index][0] <= self.max_weight:
                        # If it's possible, we add the value to our accumulated value and the weight to accumulated weight
                        self.acc_val += self.data[index][1]
                        self.acc_weight += self.data[index][0]
                        used = True
                        # We then check if the new accumulated value is bigger than what we ever saw
                        if self.lowerbound < self.acc_val:
                            self.lowerbound = self.acc_val  # If yes, we update
                        # And now if we are not at the end of the list, we DFS to the next node
                        if index + 1 < len(self.data):
                            self.dfs(index + 1)
                    else:
                        continue
                else:  # If we choose to skip this node
                    # The uppercase value decreases
                    self.upperbound -= self.data[index][1]
                    # And now if we are not at the end of the list, we DFS to the next node
                    if index + 1 < len(self.data):
                        self.dfs(index + 1)

                    # After coming back to the node, we return it's value to the upperbound
                    self.upperbound += self.data[index][1]

            # If we used it then subtract the added parameters
            if used:
                self.acc_val -= self.data[index][1]
                self.acc_weight -= self.data[index][0]
            return self.lowerbound

    d = DFS(k['weight'], k['value'], k['weight_limit'])

    print(datetime.datetime.now())
    print(d.dfs(0))
    print(datetime.datetime.now())

if __name__ == '__main__':
    main()