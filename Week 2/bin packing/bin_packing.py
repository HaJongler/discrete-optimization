import math
from copy import deepcopy
from sys import stdin


class BinPacking(object):
    def __init__(self, bin_capacity, items_weights):
        self.bin_capacity = bin_capacity
        self.items_weights = sorted(enumerate(items_weights),
                                    key=lambda index_weight: index_weight[1],
                                    reverse=True)

    def lowest_required_bins(self, index, current_bins):
        """
        For a given index and bin status, this function returns the minimal
        amount of bins required to also contain the next items, assuming that
        the items are "liquid".
        """
        max_free_space_in_current_bins = max(*[self.bin_capacity - used_weight for used_weight in current_bins])
        unpackable_items = sum([item[1] for item in self.items_weights[index:] if item[1] > max_free_space_in_current_bins])
        return math.ceil(unpackable_items / self.bin_capacity)

    def greedy_min_bins(self):
        bins = []
        # For every item in out list we try to find place in one of the existing bins
        for item_weight in self.items_weights:
            found_place_in_bins = False
            # Iterate over the existing bins
            for bin_index, bin_weight in enumerate(bins):
                # Check if the bin can be filled with the item
                if bin_weight + item_weight[1] <= self.bin_capacity:
                    bins[bin_index] += item_weight[1]
                    found_place_in_bins = True
                    break
            # If we didn't find a place we create a new bin
            if not found_place_in_bins:
                bins.append(item_weight[1])

        return bins

    def find_min(self):
        # Initialize the bins of the items
        first_items_bins = {self.items_weights[0][0]: 1}
        best_items_bins = dict()
        # Initialize the best amount of bins using greedy
        best_bins = self.greedy_min_bins()
        # Initialize the bins with one bin containing the first item's weight
        first_bins = [self.items_weights[0][1]]
        # Initialize a stack of <node, bins_weights, items_bins>
        stack = [(1, first_bins, first_items_bins)]
        # Start DFSing
        while stack:
            node, past_bins, past_items_bins = stack.pop()
            # Check if it is even possible to add the current item to the existing bins
            found_place_in_bins = False
            for bin_index, bin_weight in enumerate(past_bins):
                # Check if the bin can be filled with the item
                if bin_weight + self.items_weights[node][1] <= self.bin_capacity:
                    found_place_in_bins = True
                    # Create a new option for bins (we deepcopy in order for past_bins to say the same for other options)
                    possible_bins = deepcopy(past_bins)
                    possible_bins[bin_index] += self.items_weights[node][1]
                    # Also remember items bins
                    possible_items_bins = deepcopy(past_items_bins)
                    possible_items_bins[self.items_weights[node][0]] = bin_index + 1
                    # Try to traverse forward
                    if node + 1 < len(self.items_weights):
                        stack.append((node + 1, possible_bins, possible_items_bins))
                    else:
                        if len(best_bins) >= len(possible_bins):
                            best_bins = possible_bins
                            best_items_bins = possible_items_bins

            # Now if we traversed all bins, and couldn't find a place for our item, we open a new bin
            if not found_place_in_bins:
                # Create a new bin
                past_bins.append(self.items_weights[node][1])
                past_items_bins[self.items_weights[node][0]] = len(past_bins)
                # If we add a bin, and there's a chance to beat the best bound for bins in the future, we traverse
                if len(past_bins) + self.lowest_required_bins(node + 1, past_bins) <= len(best_bins):
                    # If we didn't reach the last item, traverse
                    if node + 1 < len(self.items_weights):
                        stack.append((node + 1, past_bins, past_items_bins))
                    else:  # Checkout our solution
                        if len(best_bins) > len(past_bins):
                            best_bins = past_bins
                            best_items_bins = past_items_bins

        return best_items_bins


def main():
    n = int(stdin.readline())
    bin_capacity = int(stdin.readline())
    items_weights = [int(x) for x in stdin.readlines()]

    bp = BinPacking(bin_capacity, items_weights)
    bins = bp.find_min()
    print(*[bins[item] for item in range(n)], sep=" ")


if __name__ == '__main__':
    main()
