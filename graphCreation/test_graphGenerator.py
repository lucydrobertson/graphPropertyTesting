from unittest import TestCase

from BoundedDegreeGraphs.boundedDegreeGraphTester import test_bd_colouring
from DenseGraphs.denseGraphTester import decide_bipartiteness
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
            if test_bd_colouring(colouring, bd_bpt_graph):
                bipartite = True
                break
        assert bipartite
