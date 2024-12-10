from unittest import TestCase
from denseGraphCreator import dense_graph_creator


class TestDenseGraph(TestCase):
    def test_is_edge(self):
        graph = dense_graph_creator([[0, 1], [1, 2], [2, 0], [2, 3]], True)
        assert graph.is_edge(0, 1)
        assert graph.is_edge(1, 2)
        assert graph.is_edge(2, 0)
        assert graph.is_edge(0, 2)
        assert not graph.is_edge(0, 3)

    def test_add_edge(self):
        graph = dense_graph_creator([[0, 1], [1, 2], [2, 0], [2, 3]], True)
        graph.add_edge(1, 3)
        assert graph.is_edge(1, 3)

    def test_get_size(self):
        graph = dense_graph_creator([[0, 1], [1, 2], [2, 0], [2, 3]], True)
        assert graph.get_size() == 4

    def test_visualise(self):
        graph = dense_graph_creator([[0, 1], [1, 2], [2, 0], [2, 3]], True)
        graph.visualise_graph()