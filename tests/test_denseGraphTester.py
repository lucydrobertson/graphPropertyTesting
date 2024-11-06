from unittest import TestCase
from denseGraphCreator import dense_graph_creator
from denseGraphTesters.denseGraphTester import DenseGraphTester, test_colouring


def majority_test(test_func):
    outcomes = 0
    # tester should be correct with probability 2/3
    # so test 3 times and take majority decision to test alg correctness
    for x in range(0, 3):
        o = test_func()
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

    def test_test_k_colourability(self):
        dense_3_col_graph = dense_graph_creator(
            [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0], [1, 4], [0, 4]], True)
        # having to use epsilon > 1 to choose fraction of vertices due to polynomial factor k in algorithm when picking
        three_col_tester = DenseGraphTester(dense_3_col_graph, 1.8)
        three_col_func = lambda: three_col_tester.test_k_colourability(3)
        assert majority_test(three_col_func)

        dense_not_3_col_graph = dense_graph_creator(
            [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0], [1, 4], [0, 4], [1, 5], [1, 3], [3, 0], [3, 5], [2, 5]], True)
        not_3col_tester = DenseGraphTester(dense_not_3_col_graph, 1)
        not_3col_func = lambda: not_3col_tester.test_k_colourability(3)
        assert not majority_test(not_3col_func)

    def test_test_colouring(self):
        graph = dense_graph_creator([[0, 1], [1, 2], [2, 0]], True)
        true_colouring = [0, 1, 2]
        assert test_colouring(graph, true_colouring)

        false_colouring = [0, 0, 1]
        assert not test_colouring(graph, false_colouring)
