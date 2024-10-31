from unittest import TestCase
from denseGraphCreator import dense_graph_creator
from denseGraphTesters.denseGraphTester import DenseGraphTester


class TestDenseGraphTester(TestCase):
    def test_construct_induced_subgraph(self):
        dense_bipartite_graph = dense_graph_creator([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0], [1, 4]], True)
        tester = DenseGraphTester(dense_bipartite_graph, 1 / 6)
        vertices_chosen = [0, 1, 2]
        manual_subgraph = dense_graph_creator([[0, 1], [1, 2]], 3)
        generated_subgraph = tester.construct_induced_subgraph(vertices_chosen)
        assert manual_subgraph.get_size() == generated_subgraph.get_size()
        assert manual_subgraph.adj_matrix == generated_subgraph.adj_matrix

    def test_test_bipartiteness(self):
        dense_bipartite_graph = dense_graph_creator([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0], [1, 4]], True)
        tester = DenseGraphTester(dense_bipartite_graph, 0.5)
        assert tester.test_bipartiteness()

