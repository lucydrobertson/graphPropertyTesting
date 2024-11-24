from unittest import TestCase

from BoundedDegreeGraphs.boundedDegreeGraph import BoundedDegreeGraph


class TestBoundedDegreeGraph(TestCase):
    def test_get_neighbours(self):
        # test that get neighbours function returns correct list of neighbours
        bd_graph = BoundedDegreeGraph(3, 3, {0: [1, 2], 1: [0], 2: [0]}, False)
        assert bd_graph.get_neighbours(0) == [1, 2]
        assert bd_graph.get_neighbours(1) == [0]
        assert bd_graph.get_neighbours(2) == [0]

    def test_add_neighbour(self):
        # test that neighbours are added bidirectionally for undirected graphs
        bd_graph = BoundedDegreeGraph(3, 3, {0: [1, 2], 1: [0], 2: [0]}, False)
        bd_graph.add_neighbour(1, 2)
        assert bd_graph.get_neighbours(1) == [0, 2]
        assert bd_graph.get_neighbours(2) == [0, 1]

        # ensure that neighbours are added uni-directionally for directed graphs
        directed_bd_graph = BoundedDegreeGraph(3, 3, {0: [1, 2], 1: [0], 2: [0]}, True)
        directed_bd_graph.add_neighbour(1, 2)
        assert directed_bd_graph.get_neighbours(1) == [0, 2]
        assert directed_bd_graph.get_neighbours(2) == [0]

    def test_get_size(self):
        # test that graph size returned matches expected value
        bd_graph = BoundedDegreeGraph(3, 3, {0: [1, 2], 1: [0], 2: [0]}, False)
        assert bd_graph.get_size() == 3

    def test_get_degree(self):
        # test that graph degree returned matches expected value
        bd_graph = BoundedDegreeGraph(3, 3, {0: [1, 2], 1: [0], 2: [0]}, False)
        assert bd_graph.get_degree() == 3
