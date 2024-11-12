import random

from DenseGraphs.denseGraph import DenseGraph


class DenseGraphGenerator:
    def __init__(self):
        pass

    def generate_bipartite_graph(self, size):
        # generate |size| nodes and probabilistically assign them to set a or set b
        # then generate some k * |size|**2 number of edges connecting the two sets
        # idea: maybe have some parameter for degree regularity or some standard deviation from it?
        # idea: have the probability of assignment to set a or b as a new parameter?

        # create an empty graph of size |size|
        bpt_graph = DenseGraph(size, [[False] * size for _ in range(0, size)])

        # assign nodes to set a or b probabilistically
        set_a = []
        set_b = []
        for x in range(0, size):
            set_choice = random.choice([True, False])
            if set_choice:
                set_a.append(x)
            else:
                set_b.append(x)

        # edge generation
        # generate k, the poly factor for n**2 edges, with a min value of 0.5 to ensure the graph is dense
        k = random.uniform(0.5, 1)
        num_edges = int(k * size**2)
        for e in range(0, num_edges):
            # for undirected graph, doesn't matter if start is in set_a or set_b
            start = random.choice(set_a)
            end = random.choice(set_b)

            # adding edges is idempotent so doesn't matter if same (start, end) pair occurs more than once
            bpt_graph.add_edge(start, end)

        return bpt_graph
