import random
from time import sleep
from copy import deepcopy

input_pattern = (
    "----------"
    "----------"
    "----------"
    "O---------"
    "O---------"
    "O---------"
    "O---------"
    "----------"
    "----------"
    "----------"
    )

patterns_to_store = [
    (
    "----OO----"
    "--OO--OO--"
    "-O------O-"
    "O--------O"
    "O--------O"
    "O--------O"
    "O--------O"
    "-O------O-"
    "--OO--OO--"
    "----OO----"
    ),
    (
    "----OO----"
    "---OOO----"
    "-----O----"
    "-----O----"
    "-----O----"
    "-----O----"
    "-----O----"
    "-----O----"
    "-----O----"
    "---OOOOO--"
    ),
    (
    "---OOOO---"
    "-OO----OO-"
    "O--------O"
    "---------O"
    "-------OO-"
    "---OOOO---"
    "-OO-------"
    "O---------"
    "O---------"
    "OOOOOOOOOO"
    )
    ]


def process_pattern(pattern):

    """
    Takes a 100 character string, pattern, and
    converts it into a list of ints; -1 for a "-" (an "off"),
    and 1 for an "O" (an "on"). Returns this list of ints.
    """
    encode = {"O":1, "-":-1}
    return [encode[c] for c in pattern]

def print_state(state):

    """
    Takes the current state of the net, state, and prints it to
    the console, followed by a divider to indicate the end of an
    iteration. Returns null.
    """

    # decode[1] == "O"
    # decode[-1] == "-"
    # "X" is included to make errors clear
    decode = ["X", "O", "-"]

    out = ""

    for y in range(0, 100, 10):
        row = ""
        for x in range(0, 10):
            row += decode[state[y + x]]
        out += row + "\n"

    print(out + "\n" + "~"*10 + "\n")


def get_initial_weights(stored_patterns, nodes):

    """
    Takes the list of processed patterns, stored_patterns, and the
    list of node values from the input pattern. Calculates initial
    weights to store the stored patterns, and stores these in a 2D
    array (first index is the start node of the connection, second
    index is the end node). Returns this 2D array.
    """

    weights = []

    for node_from in range(100):
        weights.append([])
        for node_to in range(100):
            if node_to == node_from:
                weights[node_from].append(0)
            else:
                total = 0
                for pattern in stored_patterns:
                    total += pattern[node_from] * pattern[node_to]
                weights[node_from].append(total)

    return weights


def update(nodes, weights):

    """
    Takes the current state, nodes, and updates each node in
    turn, in a random order. Returns the modified state.
    """

    update_order = [n for n in range(100)]
    random.shuffle(update_order)
    print_counter = 0

    for selected_node in update_order:
        total = 0
        for i in range(100):
            total += nodes[i] * weights[selected_node][i]

        if total > 0:
            nodes[selected_node] = 1
        elif total < 0:
            nodes[selected_node] = -1

        print_counter += 1
        if print_counter % 10 == 0: # Change frequncy of prints here
            print_state(nodes)
            sleep(0.1)
            

    return nodes


def get_random_input():

    """
    Returns a random starting state for the network.
    """

    return [random.choice([-1, 1]) for n in range(100)]


def main():

    stored_patterns = []
    for pattern in patterns_to_store:
        stored_patterns.append(process_pattern(pattern))

    nodes = process_pattern(input_pattern)
    nodes = get_random_input() # Un-comment to start with a random state

    weights = get_initial_weights(stored_patterns, nodes)

    max_iterations = 100
    last_state = []

    current_iteration = 0
    while (current_iteration < max_iterations):
        print("Iteration: " + str(current_iteration) + "\n")
        print_state(nodes)
        last_state = deepcopy(nodes)
        nodes = update(nodes, weights)

        if nodes == last_state:
            print("Stable state reached.")
            break

        current_iteration += 1

    else:
        print("Max iterations reached.")

if __name__ == "__main__":
    main()