from graphModels.denseGraph import DenseGraph

my_dense_graph = DenseGraph(4,
                      {
                          1: {2: True, 3: False, 4: True},
                          2: {3: True, 4: True},
                          3: {4: False}
                        }
                      )

print(my_dense_graph.is_edge(1, 2))
print(my_dense_graph.is_edge(2, 1))
print(my_dense_graph.is_edge(4, 3))