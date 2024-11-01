from unittest import TestCase
from denseGraphCreator import dense_graph_creator
from denseGraphTesters.denseGraphTester import DenseGraphTester


def majority_test(test_func):
    outcomes = 0
    # tester should be correct with probability 2/3
    # so test 3 times and take majority decision to test alg correctness
    for x in range(3):
        if test_func():
            outcomes += 1
    return outcomes >= 2


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
        bipartite_tester = DenseGraphTester(dense_bipartite_graph, 0.5)
        assert majority_test(bipartite_tester.test_bipartiteness)

        dense_not_bipartite_graph = dense_graph_creator([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0], [1, 4],
                                                         [1, 5], [0, 4], [1, 3]], True)
        not_bipartite_tester = DenseGraphTester(dense_not_bipartite_graph, 0.5)
        assert not majority_test(not_bipartite_tester.test_bipartiteness)

    def test_test_degree_regularity(self):
        degree_reg_graph = dense_graph_creator([[0, 1], [1, 2], [2, 3], [3, 0], [0, 2], [1, 3]], True)
        degree_reg_tester = DenseGraphTester(degree_reg_graph, 0.3)
        assert majority_test(degree_reg_tester.test_degree_regularity)

        not_degree_reg_graph = dense_graph_creator([[0, 2], [1, 2], [3, 2]], True)
        not_degree_reg_tester = DenseGraphTester(not_degree_reg_graph, 0.2)
        assert not majority_test(not_degree_reg_tester.test_degree_regularity)
