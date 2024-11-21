def generate_k_colourings(graph_size, k):
    # generate each potential k-colouring of a graph of size graph_size
    possible_colourings = []

    subgraph_size = graph_size
    for index in range(k ** subgraph_size):
        colouring = [0] * subgraph_size
        # convert the index (number of colouring) into an array representing that colouring
        # aka convert the index from base 10 to base k
        col_index = -1
        while index > 0:
            colouring[col_index] = index % k
            index = index // k
            col_index -= 1

        possible_colourings.append(colouring)

    return possible_colourings
