from unittest import TestCase

from BoundedDegreeGraphs.boundedDegreeGraph import BoundedDegreeGraph
from BoundedDegreeGraphs.boundedDegreeGraphTester import BoundedDegreeGraphTester


class TestBoundedDegreeGraphTester(TestCase):
    def test_choose_vertices(self):
        graph = BoundedDegreeGraph(5, 4, {0: [1, 2, 3, 4], 1: [0, 2, 3], 2: [0, 1, 4], 3: [0, 1], 4: [0, 2]}, False)
        tester = BoundedDegreeGraphTester(graph, 1/6)
        # choose vertices randomly from graph, duplicates are likely to exist
        # so we ony want the number chosen to be close to what is expected
        assert len(tester.choose_vertices(3)) >= 2

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

    def test_breadth_first_search_find_cycle(self):
        cycle_free_graph = BoundedDegreeGraph(5, 2, {0: [1, 2], 1: [0, 4], 2: [0, 3], 3:[2, 5], 4: [1], 5: [3]}, False)
        cycle_free_tester = BoundedDegreeGraphTester(cycle_free_graph, 1/3)
        contains_cycle, num_explored = cycle_free_tester.breadth_first_search_find_cycle(0, 5)
        assert not contains_cycle
        assert num_explored == 5

        contains_cycle, num_explored = cycle_free_tester.breadth_first_search_find_cycle(0, 3)
        assert not contains_cycle
        assert num_explored == 3

        cycle_containing_graph = BoundedDegreeGraph(5, 4, {0: [1, 2, 3, 4], 1: [0, 2, 3], 2: [0, 1, 4], 3: [0, 1], 4: [0, 2]}, False)
        cycle_tester = BoundedDegreeGraphTester(cycle_containing_graph, 1/3)
        contains_cycle, num_explored = cycle_tester.breadth_first_search_find_cycle(0, 5)
        assert contains_cycle

    def test_test_cycle_freeness(self):
        cycle_free_graph = BoundedDegreeGraph(5, 2, {0: [1, 2], 1: [0, 4], 2: [0, 3], 3:[2, 5], 4: [1], 5: [3]}, False)
        cycle_free_tester = BoundedDegreeGraphTester(cycle_free_graph, 1/6)
        assert cycle_free_tester.test_cycle_freeness()

        cycle_containing_graph = BoundedDegreeGraph(5, 4,{0: [1, 2, 3, 4], 1: [0, 2, 3], 2: [0, 1, 4], 3: [0, 1], 4: [0, 2]},False)
        cycle_tester = BoundedDegreeGraphTester(cycle_containing_graph, 1 / 6)
        assert not cycle_tester.test_cycle_freeness()

    def test_get_vertices_in_radius(self):
        graph = BoundedDegreeGraph(6, 3, {0: [1], 1: [0, 2, 5], 2: [1, 3], 3: [2, 4], 4: [4], 5: [1]}, False)
        vertex_distance_tester = BoundedDegreeGraphTester(graph, 1/6)
        # test that only vertex reachable at distance 0 is the start vertex
        assert vertex_distance_tester.get_vertices_in_radius(0, 0) == [0]
        # test vertices reachable for some distance in the graph
        assert vertex_distance_tester.get_vertices_in_radius(0, 2) == [0, 1, 2, 5]
        # test that all vertices are returned if distance is greater than the graphs diameter
        assert vertex_distance_tester.get_vertices_in_radius(0, 8) == [0, 1, 2, 3, 4, 5]

    def test_create_induced_subgraph(self):
        graph = BoundedDegreeGraph(6, 3, {0: [1], 1: [0, 2, 5], 2: [1, 3], 3: [2, 4], 4: [4], 5: [1]}, False)
        subgraph_tester = BoundedDegreeGraphTester(graph, 1/6)
        subgraph_vertices = [0, 1, 2, 5]
        subgraph = subgraph_tester.create_induced_subgraph(subgraph_vertices)
        assert subgraph.get_size() == 4
        assert subgraph.degree == graph.get_degree()
        # note that subgraph vertices are renamed so that vertex 5 becomes vertex 3
        assert subgraph.inc_func == {0: [1], 1: [0, 2, 5], 2: [1], 3: [1]}
        assert subgraph.get_directed() == graph.get_directed()

    def test_test_sparse_k_colourability(self):
        Three_col_bd_graph = BoundedDegreeGraph(6, 4, {0: [1, 4, 5], 1: [0, 2, 4], 2: [1, 3], 3: [2, 4], 4: [0, 1, 3, 5], 5: [0, 4]}, False)
        kcol_tester = BoundedDegreeGraphTester(Three_col_bd_graph, 1/6)
        assert kcol_tester.test_sparse_k_colourability(3)

        not_three_col_bd_graph = BoundedDegreeGraph(6, 5, {0: [1, 4, 5], 1: [0, 2, 4, 5], 2: [1, 3, 4], 3: [2, 4], 4: [0, 1, 2, 3, 5], 5: [0, 1, 4]}, False)
        not_kcol_tester = BoundedDegreeGraphTester(not_three_col_bd_graph, 1/6)
        assert not not_kcol_tester.test_sparse_k_colourability(3)
