from graphModels.denseGraph import DenseGraph




@Test
def test_edges_exist():
    graph = dense_graph_creator([[0, 1], [1, 2], [2, 0], [2, 3]], True)
    assert graph.is_edge(0, 1)
    assert graph.is_edge(1, 2)
    assert graph.is_edge(2, 0)
    assert graph.is_edge(0, 2)
    assert not graph.is_edge(0, 3)




