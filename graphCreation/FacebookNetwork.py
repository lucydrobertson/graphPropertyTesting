# data from facebook social networks
# downloaded from https://snap.stanford.edu/data/ego-Facebook.html
from BoundedDegreeGraphs.boundedDegreeGraph import BoundedDegreeGraph
from BoundedDegreeGraphs.boundedDegreeGraphTester import BoundedDegreeGraphTester


def import_edges():
    edge_file = open("facebook_edges.txt", "r")
    edges = edge_file.read().split("\n")

    clean_edges = []
    for edge_line in edges:
        edge = edge_line.split(" ")
        if len(edge) > 1:
            clean_edges.append((int(edge[0]), int(edge[1])))
        else:
            print("Not an edge between two nodes: ", edge)

    return clean_edges


def convert_edges_to_bounded_degree_graph(edge_list):
    # create empty graph, note that Facebook networks are undirected
    # the dataset consists of 4039 nodes
    graph = BoundedDegreeGraph(0, 0, {}, False)

    for edge in edge_list:
        try:
            graph.add_neighbour(edge[0], edge[1])
        except ValueError:
            graph.increment_degree()
            graph.add_neighbour(edge[0], edge[1])

    graph.size = len(graph.inc_func.keys())
    print("size ", graph.get_size())
    return graph


if __name__ == "__main__":
    edges = import_edges()
    # the dataset should contain 88234 edges according to its datasheet
    assert len(edges) == 88234

    facebook_network = convert_edges_to_bounded_degree_graph(edges)

    expander_tester = BoundedDegreeGraphTester(facebook_network, 1/20)
    expander_bool = expander_tester.test_expansion(1/4)
    if expander_bool:
        print("The Facebook social network graph is an expander graph with alpha = 1/4")
    else:
        print("Not an expander")
