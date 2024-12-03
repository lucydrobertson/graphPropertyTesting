from unittest import TestCase

from BoundedDegreeGraphs.boundedDegreeGraphTester import test_bd_colouring
from DenseGraphs.denseGraphTester import decide_bipartiteness, DenseGraphTester, test_dense_colouring
from create_k_colourings import generate_k_colourings
from graphCreation.graphGenerator import GraphGenerator


class TestGraphGenerator(TestCase):
    def test_convert_to_dense(self):
        self.fail()

    def test_convert_to_bounded_degree(self):
        self.fail()

    def test_generate_bipartite_graph(self):
        dense_generator = GraphGenerator(True, False)
        dense_bpt_graph = dense_generator.generate_bipartite_graph(20)

        # decide if dense_bpt_graph is bipartite, it should be
        assert decide_bipartiteness(dense_bpt_graph)

        bd_generator = GraphGenerator(False, False)
        bd_bpt_graph = bd_generator.generate_bipartite_graph(20)

        # decide if bd_bpt_graph is bipartite, by checking that it's 2-colourable
        # this is done in exponential time, so only really suitable for small graph sizes
        # hence the need for property testing in the first place!
        colourings = generate_k_colourings(bd_bpt_graph.get_size(), 2)
        bipartite = False
        for colouring in colourings:
            if test_bd_colouring(bd_bpt_graph, colouring):
                bipartite = True
                break
        assert bipartite

    def test_generate_k_col_graph(self):
        k = 3
        dense_generator = GraphGenerator(True, False)
        dense_k_col_graph = dense_generator.generate_k_col_graph(10, k)

        bounded_degree_generator = GraphGenerator(False, False)
        bd_k_col_graph = bounded_degree_generator.generate_k_col_graph(10, k)

        for (kcol_graph, test_graph_colouring) in [(dense_k_col_graph, test_dense_colouring),
                                               (bd_k_col_graph, test_bd_colouring)]:
            colourings = generate_k_colourings(kcol_graph.get_size(), k)
            k_colourable = False
            for colouring in colourings:
                if test_graph_colouring(kcol_graph, colouring):
                    k_colourable = True
                    break
            assert k_colourable

    def test_generate_degree_regular_graph(self):
        # ran this for 10,000 iterations and it didn't fail so pretty sure the alg is correct
        chosen_degree = 12
        degree_reg_generator = GraphGenerator(False, False)
        graph = degree_reg_generator.generate_degree_regular_graph(25, chosen_degree)

        degrees = [len(node_neighbours) for node, node_neighbours in graph.inc_func.items()]
        for d in degrees:
            assert d == chosen_degree
