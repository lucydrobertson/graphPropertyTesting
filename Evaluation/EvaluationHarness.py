from DenseGraphs.denseGraphTester import DenseGraphTester
from BoundedDegreeGraphs.boundedDegreeGraphTester import BoundedDegreeGraphTester
from Evaluation.evalutor import Evaluator
from graphCreation.graphGenerator import GraphGenerator


class EvaluationHarness:
    def __init__(self, graph_sizes, epsilon_values, directed):
        self.graph_sizes = graph_sizes  # [10, 25, 100, 250, 1000]
        self.epsilons = epsilon_values  # [1/10, 1/6, 1/4, 1/3, 1/2]
        self.directed = directed

    # each method generates a graph with that property
    # then creates a tester object and passes the correct property testing method to an Evaluator object
    # which then creates a file of the results
    # then repeat for a graph that is e-far from having the property
    def evaluate_dense_bipartiteness_tester(self, num_iterations):
        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                graph_generator = GraphGenerator(True, self.directed, epsilon)

                # evaluate property tester on graph that is bipartite
                bpt_graph = graph_generator.generate_bipartite_graph(size)
                bpt_tester = DenseGraphTester(bpt_graph, epsilon)
                test_description = f"Dense bipartiteness tester evaluation on bipartite graph of size {size}"
                bpt_evaluator = Evaluator(bpt_tester.test_bipartiteness, test_description, False)
                bpt_evaluator.test_method(num_iterations)

                # evaluate property tester on graph that is epsilon far from being bipartite
                not_bpt_graph = graph_generator.generate_e_far_from_bipartite_graph(size)
                not_bpt_tester = DenseGraphTester(not_bpt_graph, epsilon)
                test_description = (f"Dense bipartiteness tester evaluation on epsilon-far from bipartite graph"
                                    f" of size {size} with epsilon {round(epsilon, 2)}")
                not_bpt_evaluator = Evaluator(not_bpt_tester.test_bipartiteness, test_description, True)
                not_bpt_evaluator.test_method(num_iterations)

    def evaluate_dense_k_colourability_tester(self):
        pass

    def evaluate_dense_degree_regularity_tester(self):
        pass

    def evaluate_bounded_degree_bipartiteness_tester(self):
        pass

    def evaluate_bounded_degree_k_colourability_tester(self):
        pass

    def evaluate_bounded_degree_cycle_freeness_tester(self):
        pass
