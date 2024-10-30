from unittest import TestCase
from graphModels.denseGraph import DenseGraph


def dense_graph_creator(edges, undirected):
    vertices = []
    for edge in edges:
        for vertex in edge:
            if vertex not in vertices:
                vertices.append(vertex)

    graph = [[False] * len(vertices) for _ in range(len(vertices))]
    for edge in edges:
        graph[edge[0]][edge[1]] = True
        if undirected:
            graph[edge[1]][edge[0]] = True
    return DenseGraph(len(vertices), graph)


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

dense_bipartite_graph = dense_graph_creator([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0], [1, 4]], True)