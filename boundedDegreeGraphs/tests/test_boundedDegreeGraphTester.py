from unittest import TestCase

from boundedDegreeGraphs.boundedDegreeGraph import BoundedDegreeGraph
from boundedDegreeGraphs.boundedDegreeGraphTester import BoundedDegreeGraphTester


class TestBoundedDegreeGraphTester(TestCase):
    def test_choose_vertices(self):
        self.fail()

    def test_odd_cycle(self):
        graph_with_odd_cycle = BoundedDegreeGraph(5, 4, {0: [1, 2, 3, 4], 1: [0, 2, 3], 2: [0, 1, 4], 3: [0, 1], 4: [0, 2]}, False)
        tester_odd = BoundedDegreeGraphTester(graph_with_odd_cycle, 1/3)
        assert tester_odd.odd_cycle(0)

        graph_without_odd_cycle = BoundedDegreeGraph(5, 4, {0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}, False)
        tester_not_odd = BoundedDegreeGraphTester(graph_without_odd_cycle, 1/3)
        assert not tester_not_odd.odd_cycle(0)

    def test_test_bipartiteness(self):
        bpt_graph = BoundedDegreeGraph(5, 4, {0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}, False)
        bpt_tester = BoundedDegreeGraphTester(bpt_graph, 1/3)
        assert bpt_tester.test_bipartiteness()

        not_bpt_graph = BoundedDegreeGraph(5, 4, {0: [1, 2, 3, 4], 1: [0, 2, 3], 2: [0, 1, 4], 3: [0, 1], 4: [0, 2]}, False)
        not_bpt_tester = BoundedDegreeGraphTester(not_bpt_graph, 1/3)
        assert not not_bpt_tester.test_bipartiteness()
