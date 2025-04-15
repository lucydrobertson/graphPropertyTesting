from DenseGraphs.denseGraph import DenseGraph
from DenseGraphs.denseGraphTester import DenseGraphTester


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


dense_bipartite_graph = dense_graph_creator(
    [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0], [1, 4]],
    True
)