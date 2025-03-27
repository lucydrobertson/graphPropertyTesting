def generate_k_colourings(graph_size, k):
    # generate each potential k-colouring of a graph of size graph_size
    possible_colourings = []

    for index in range(k ** graph_size):
        colouring = generate_k_colouring_from_index(index, graph_size, k)
        possible_colourings.append(colouring)
    return possible_colourings


def generate_k_colouring_from_index(index, graph_size, k):
    colouring = [0] * graph_size
    # convert the index (number of colouring) into an array representing that colouring
    col_index = -1
    while index > 0:
        colouring[col_index] = index % k
        index = index // k
        col_index -= 1
    return colouring
