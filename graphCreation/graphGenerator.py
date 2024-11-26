import math
import random

from BoundedDegreeGraphs.boundedDegreeGraph import BoundedDegreeGraph
from DenseGraphs.denseGraph import DenseGraph


class GraphGenerator:
    def __init__(self, dense, directed):
        # boolean: True for dense graph, false for bounded degree (sparse) graph
        self.dense = dense
        self.directed = directed

    # converts a list of edges to a dense graph
    def convert_to_dense(self, graph_size, graph_edges):
        graph = DenseGraph(graph_size, [[False] * graph_size for _ in range(0, graph_size)])
        for edge in graph_edges:
            graph.add_edge(edge[0], edge[1])
            if not self.directed:
                graph.add_edge(edge[1], edge[0])
        return graph

    def convert_to_bounded_degree(self, graph_size, max_degree, graph_edges):
        # create empty graph
        graph = BoundedDegreeGraph(graph_size, max_degree, {}, self.directed)
        for edge in graph_edges:
            graph.add_neighbour(edge[0], edge[1])
        return graph

    def generate_bipartite_graph(self, size):
        # generate |size| nodes and probabilistically assign them to set a or set b
        # then generate some k * |size|**2 number of edges connecting the two sets
        # idea: maybe have some parameter for degree regularity or some standard deviation from it?
        # idea: have the probability of assignment to set a or b as a new parameter?

        # create an empty graph of size |size|
        bpt_graph_edges = []

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
        # generate k, the poly factor for the #edges, with a min value of 0.5 to ensure the graph has sufficient edges
        k = random.uniform(0.5, 1)
        if self.dense:
            num_edges = int(k * size**2)
        # for a sparse graph, have some k*nlogn edges
        else:
            num_edges = int(k * size * math.log2(size))

        for e in range(0, num_edges):
            # for undirected graph, doesn't matter if start is in set_a or set_b
            start = random.choice(set_a)
            end = random.choice(set_b)

            # during graph conversion, adding edges is idempotent
            # so doesn't matter if same (start, end) pair occurs more than once
            bpt_graph_edges.append([start, end])

        if self.dense:
            return self.convert_to_dense(size, bpt_graph_edges)
        else:
            # arbitrarily set max_degree to 5*log2(size of graph)
            # TO DO: decide if this is a good choice, maybe it should be a parameter??
            return self.convert_to_bounded_degree(size, math.log2(size)*5, bpt_graph_edges)
