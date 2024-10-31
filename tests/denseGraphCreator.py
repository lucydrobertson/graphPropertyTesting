from graphModels.denseGraph import DenseGraph


def dense_graph_creator(edges, undirected):
    vertices = []
    for edge in edges:
        for vertex in edge:
            if vertex not in vertices:
                vertices.append(vertex)

    graph = [[False] * len(vertices) for _ in range(len(vertices))]

    # a node has an edge to itself (of length 0) to avoid errors later on
    for vertex in vertices:
        graph[vertex][vertex] = True

    for edge in edges:
        graph[edge[0]][edge[1]] = True
        if undirected:
            graph[edge[1]][edge[0]] = True
    return DenseGraph(len(vertices), graph)
