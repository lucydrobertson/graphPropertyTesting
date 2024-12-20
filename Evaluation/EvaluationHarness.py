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

    def evaluate_dense_k_colourability_tester(self, num_iterations, k):
        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                graph_generator = GraphGenerator(True, self.directed, epsilon)

                # evaluate property tester on graph that is k-colourable
                k_col_graph = graph_generator.generate_k_col_graph(size, k)
                k_col_tester = DenseGraphTester(k_col_graph, epsilon)
                test_description = f"Dense K-colourability tester evaluation on {k}-colourable graph of size {size}"
                k_col_evaluator = Evaluator(lambda: k_col_tester.test_k_colourability(k), test_description, False)
                k_col_evaluator.test_method(num_iterations)

                # evaluate property tester on graph that is epsilon far from being k-colourable
                not_k_col_graph = graph_generator.generate_e_far_from_k_col_graph(size, k)
                not_k_col_tester = DenseGraphTester(not_k_col_graph, epsilon)
                test_description = (f"Dense k-colourability tester evaluation on epsilon-far from "
                                    f"{k}-colourable graph of size {size} with epsilon {round(epsilon, 2)}"
                                    f" of size {size} with epsilon {round(epsilon, 2)}")
                not_k_col_evaluator = Evaluator(lambda: not_k_col_tester.test_k_colourability(k), test_description, True)
                not_k_col_evaluator.test_method(num_iterations)

    def evaluate_dense_degree_regularity_tester(self, num_iterations, degree):
        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                graph_generator = GraphGenerator(True, self.directed, epsilon)

                regular_graph = graph_generator.generate_degree_regular_graph(size, degree)
                regularity_tester = DenseGraphTester(regular_graph, epsilon)
                test_description = f"Dense degree regularity tester evaluation on regular graph of size {size}"
                regular_evaluator = Evaluator(regularity_tester.test_degree_regularity, test_description, False)
                regular_evaluator.test_method(num_iterations)

                irregular_graph = graph_generator.generate_e_far_from_degree_regular_graph(size, degree)
                irregularity_tester = DenseGraphTester(irregular_graph, epsilon)
                irregular_test_description = (f"Dense degree regularity tester evaluation on epsilon far from regular"
                                              f" graph of size {size} with epsilon {round(epsilon, 2)}")
                irregular_evaluator = Evaluator(irregularity_tester.test_degree_regularity, irregular_test_description,
                                                False)
                irregular_evaluator.test_method(num_iterations)

    def evaluate_bounded_degree_bipartiteness_tester(self):
        pass

    def evaluate_bounded_degree_k_colourability_tester(self):
        pass

    def evaluate_bounded_degree_cycle_freeness_tester(self):
        pass
