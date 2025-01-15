from DenseGraphs.denseGraphTester import DenseGraphTester
from BoundedDegreeGraphs.boundedDegreeGraphTester import BoundedDegreeGraphTester
from Evaluation.Evalutor import Evaluator
from graphCreation.graphGenerator import GraphGenerator
import datetime


# idea! have evaluator take in an array of graph property testers, so that it can run on that array
# will simplify the whole process, but still pass in filename as it's cleaner


class EvaluationHarness:
    def __init__(self, graph_sizes, epsilon_values, directed):
        self.graph_sizes = graph_sizes  # [10, 25, 100, 250, 1000]
        self.epsilons = epsilon_values  # [1/10, 1/6, 1/4, 1/3, 1/2]
        self.directed = directed

    # each method generates a graph with that property
    # then creates a tester object and passes the correct property testing method to an Evaluator object
    # which then creates a file of the results
    # then repeat for a graph that is e-far from having the property
    def evaluate_dense_bipartiteness_tester(self, num_iterations_per_graph, num_graphs_to_test):
        e_far_filename = ("dense_bipartiteness_tester_epsilon_far:_" +
                          datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))
        prop_filename = "dense_bipartiteness_tester:_" + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')

        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                graph_generator = GraphGenerator(True, self.directed, epsilon)

                bpt_testers = [DenseGraphTester(
                    graph_generator.generate_bipartite_graph(size),
                    epsilon
                ).test_bipartiteness for _ in range(0, num_graphs_to_test)]

                test_description = (f"Dense bipartiteness tester evaluation on bipartite graph of size {size}"
                                    f" using epsilon {round(epsilon, 2)}\n")
                bpt_evaluator = Evaluator(prop_filename, bpt_testers, test_description, False)
                bpt_evaluator.test_method(num_iterations_per_graph)

                # evaluate property tester on graph that is epsilon far from being bipartite
                not_bpt_testers = [DenseGraphTester(
                    graph_generator.generate_e_far_from_bipartite_graph(size),
                    epsilon
                ).test_bipartiteness for _ in range(0, num_graphs_to_test)]
                test_description = (f"Dense bipartiteness tester evaluation on epsilon-far from bipartite graph"
                                    f" of size {size} with epsilon {round(epsilon, 2)}\n")
                not_bpt_evaluator = Evaluator(e_far_filename, not_bpt_testers, test_description, True)
                not_bpt_evaluator.test_method(num_iterations_per_graph)

    def evaluate_dense_k_colourability_tester(self, num_iterations_per_graph, num_graphs_to_test, k):
        e_far_filename = ("dense_k_colourability_tester_epsilon_far:_" +
                          datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))
        prop_filename = "dense_k_colourability_tester:_" + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')

        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                graph_generator = GraphGenerator(True, self.directed, epsilon)

                # evaluate property tester on graph that is k-colourable
                k_col_testers = [lambda: DenseGraphTester(graph_generator.generate_k_col_graph(size, k),
                                                          epsilon).test_k_colourability(k)
                                 for _ in range(0, num_graphs_to_test)]
                prop_test_description = (
                    f"Dense K-colourability tester evaluation on {k}-colourable graph of size {size}"
                    f"using epsilon {round(epsilon, 2)}\n")
                k_col_evaluator = Evaluator(prop_filename, k_col_testers, prop_test_description, False)
                k_col_evaluator.test_method(num_iterations_per_graph)

                # evaluate property tester on graph that is epsilon far from being k-colourable
                not_k_col_testers = [lambda: DenseGraphTester(graph_generator.generate_e_far_from_k_col_graph(size, k),
                                                              epsilon).test_k_colourability(k)
                                     for _ in range(0, num_graphs_to_test)]
                e_far_test_description = (
                    f"Dense k-colourability tester evaluation on epsilon-far from "
                    f"{k}-colourable graph of size {size} with epsilon {round(epsilon, 2)}\n")
                not_k_col_evaluator = Evaluator(e_far_filename, not_k_col_testers, e_far_test_description, True)
                not_k_col_evaluator.test_method(num_iterations_per_graph)

    def evaluate_dense_degree_regularity_tester(self, num_iterations, degree):
        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                graph_generator = GraphGenerator(True, self.directed, epsilon)

                regular_graph = graph_generator.generate_degree_regular_graph(size, degree)
                regularity_tester = DenseGraphTester(regular_graph, epsilon)
                test_description = (f"Dense degree regularity tester evaluation on regular graph of size {size}"
                                    f"using epsilon {round(epsilon, 2)}")
                regular_evaluator = Evaluator(regularity_tester.test_degree_regularity, test_description, False)
                regular_evaluator.test_method(num_iterations)

                irregular_graph = graph_generator.generate_e_far_from_degree_regular_graph(size, degree)
                irregularity_tester = DenseGraphTester(irregular_graph, epsilon)
                irregular_test_description = (f"Dense degree regularity tester evaluation on epsilon far from regular"
                                              f" graph of size {size} with epsilon {round(epsilon, 2)}")
                irregular_evaluator = Evaluator(irregularity_tester.test_degree_regularity, irregular_test_description,
                                                False)
                irregular_evaluator.test_method(num_iterations)

    def evaluate_bounded_degree_bipartiteness_tester(self, num_iterations):
        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                graph_generator = GraphGenerator(False, self.directed, epsilon)

                bpt_graph = graph_generator.generate_bipartite_graph(size)
                bpt_tester = BoundedDegreeGraphTester(bpt_graph, epsilon)
                bpt_test_description = (f"Bounded-degree bipartiteness tester evaluation on bipartite graph "
                                        f"of size {size} using epsilon {round(epsilon, 2)}")
                bpt_evaluator = Evaluator(bpt_tester.test_bipartiteness, bpt_test_description, False)
                bpt_evaluator.test_method(num_iterations)

                not_bpt_graph = graph_generator.generate_e_far_from_bipartite_graph(size)
                not_bpt_tester = BoundedDegreeGraphTester(not_bpt_graph, epsilon)
                not_bpt_test_description = (f"Bounded-degree bipartiteness tester evaluation on epsilon far from "
                                            f"bipartite graph of size {size} with epsilon {round(epsilon, 2)}")
                not_bpt_evaluator = Evaluator(not_bpt_tester.test_bipartiteness, not_bpt_test_description, True)
                not_bpt_evaluator.test_method(num_iterations)

    def evaluate_bounded_degree_k_colourability_tester(self, num_iterations, k):
        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                graph_generator = GraphGenerator(False, self.directed, epsilon)

                k_col_graph = graph_generator.generate_k_col_graph(size, k)
                k_col_tester = BoundedDegreeGraphTester(k_col_graph, epsilon)
                k_col_test_description = (f"Bounded-degree K-colourability tester evaluation on {k}-colourable graph"
                                          f" of size {size} using epsilon {round(epsilon, 2)}")
                k_col_evaluator = Evaluator(lambda: k_col_tester.test_sparse_k_colourability(k), k_col_test_description,
                                            False)
                k_col_evaluator.test_method(num_iterations)

                not_k_col_graph = graph_generator.generate_e_far_from_k_col_graph(size, k)
                not_k_col_tester = BoundedDegreeGraphTester(not_k_col_graph, epsilon)
                not_k_col_test_description = (f"Bounded-degree k-colourability tester evaluation on epsilon-far from "
                                              f"{k}-colourable graph of size {size} with epsilon {round(epsilon, 2)}")
                not_k_col_evaluator = Evaluator(lambda: not_k_col_tester.test_sparse_k_colourability(k),
                                                not_k_col_test_description, True)
                not_k_col_evaluator.test_method(num_iterations)

    def evaluate_bounded_degree_cycle_freeness_tester(self, num_iterations):
        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                graph_generator = GraphGenerator(False, self.directed, epsilon)

                acyclic_graph = graph_generator.generate_cycle_free_graph(size)
                acyclic_tester = BoundedDegreeGraphTester(acyclic_graph, epsilon)
                acyclic_test_description = (f"Bounded-degree cycle freeness tester evaluation on cycle-free graph"
                                            f" of size {size} using epsilon {round(epsilon, 2)}")
                acyclic_evaluator = Evaluator(acyclic_tester.test_cycle_freeness, acyclic_test_description,
                                              False)
                acyclic_evaluator.test_method(num_iterations)

                cyclic_graph = graph_generator.generate_e_far_from_cycle_free_graph(size)
                cyclic_tester = BoundedDegreeGraphTester(cyclic_graph, epsilon)
                cyclic_test_description = (f"Bounded-degree cycle freeness tester evaluation on epsilon far from "
                                           f"cycle-free graph of size {size} with epsilon {round(epsilon, 2)}")
                acyclic_evaluator = Evaluator(cyclic_tester.test_cycle_freeness, cyclic_test_description, True)
                acyclic_evaluator.test_method(num_iterations)
