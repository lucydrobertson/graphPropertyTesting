from DenseGraphs.denseGraphTester import DenseGraphTester
from Evaluation.evalutionHarness import EvaluationHarness
from graphCreation.graphGenerator import GraphGenerator

if __name__ == "__main__":
    # generate graph
    # then test it 100 times with a property tester
    # using the evaluation harness

    bpt_graph = GraphGenerator(True, False, 1/8).generate_bipartite_graph(100)
    tester = DenseGraphTester(bpt_graph, 1/8)

    harness = EvaluationHarness(tester.test_bipartiteness)
    harness.test_method(100)

