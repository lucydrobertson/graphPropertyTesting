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

        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                e_far_filename = (f"dense_bipartiteness_tester_epsilon_far_{size}_{epsilon}:_" +
                                  datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))
                prop_filename = (f"dense_bipartiteness_tester_{size}_{epsilon}:_" +
                                 datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))

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

        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                e_far_filename = (f"dense_k_colourability_tester_epsilon_far_{size}_{epsilon}:_" +
                                  datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))
                prop_filename = (f"dense_k_colourability_tester_{size}_{epsilon}:_" +
                                 datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))

                graph_generator = GraphGenerator(True, self.directed, epsilon)

                # evaluate property tester on graph that is k-colourable
                k_col_testers = [lambda: DenseGraphTester(graph_generator.generate_k_col_graph(size, k),
                                                          epsilon).test_k_colourability(k)
                                 for _ in range(0, num_graphs_to_test)]
                prop_test_description = (
                    f"Dense K-colourability tester evaluation on {k}-colourable graph of size {size}"
                    f" using epsilon {round(epsilon, 2)}\n")
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

    def evaluate_dense_degree_regularity_tester(self, num_iterations_per_graph, num_graphs_to_test, degree):

        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                e_far_filename = (f"dense_regularity_tester_epsilon_far_{size}_{epsilon}:_" +
                                  datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))
                prop_filename = (f"dense_regularity_tester:__{size}_{epsilon}" +
                                 datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))

                graph_generator = GraphGenerator(True, self.directed, epsilon)

                regularity_testers = [DenseGraphTester(graph_generator.generate_degree_regular_graph(size, degree),
                                                       epsilon).test_degree_regularity
                                      for _ in range(0, num_graphs_to_test)]
                test_description = (f"Dense degree regularity tester evaluation on regular graph of size {size}"
                                    f"using epsilon {round(epsilon, 2)}\n")
                regular_evaluator = Evaluator(prop_filename, regularity_testers, test_description, False)
                regular_evaluator.test_method(num_iterations_per_graph)

                irregularity_testers = [DenseGraphTester(
                    graph_generator.generate_e_far_from_degree_regular_graph(size,degree), epsilon)
                                        .test_degree_regularity
                                        for _ in range(0, num_graphs_to_test)]
                irregular_test_description = (f"Dense degree regularity tester evaluation on epsilon far from regular"
                                              f" graph of size {size} with epsilon {round(epsilon, 2)}\n")
                irregular_evaluator = Evaluator(e_far_filename, irregularity_testers, irregular_test_description,
                                                False)
                irregular_evaluator.test_method(num_iterations_per_graph)

    def evaluate_bounded_degree_bipartiteness_tester(self, num_iterations_per_graph, num_graphs_to_test):

        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                e_far_filename = (f"bounded_degree_bipartiteness_tester_epsilon_far_{size}_{epsilon}:_" +
                                  datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))
                prop_filename = (f"bounded_degree_bipartiteness_tester_{size}_{epsilon}:_" +
                                 datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))

                graph_generator = GraphGenerator(False, self.directed, epsilon)

                bpt_testers = [BoundedDegreeGraphTester(graph_generator.generate_bipartite_graph(size), epsilon)
                               .test_bipartiteness for _ in range(0, num_graphs_to_test)]
                bpt_test_description = (f"Bounded-degree bipartiteness tester evaluation on bipartite graph "
                                        f"of size {size} using epsilon {round(epsilon, 2)}\n")
                bpt_evaluator = Evaluator(prop_filename, bpt_testers, bpt_test_description, False)
                bpt_evaluator.test_method(num_iterations_per_graph)

                not_bpt_testers = [BoundedDegreeGraphTester(graph_generator.generate_e_far_from_bipartite_graph(size),
                                                            epsilon)
                                   .test_bipartiteness for _ in range(0, num_graphs_to_test)]
                not_bpt_test_description = (f"Bounded-degree bipartiteness tester evaluation on epsilon far from "
                                            f"bipartite graph of size {size} with epsilon {round(epsilon, 2)}\n")
                not_bpt_evaluator = Evaluator(e_far_filename, not_bpt_testers, not_bpt_test_description, True)
                not_bpt_evaluator.test_method(num_iterations_per_graph)

    def evaluate_bounded_degree_k_colourability_tester(self, num_iterations_per_graph, num_graphs_to_test, k):

        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                e_far_filename = (f"bounded_degree_k_colourability_tester_epsilon_far_{size}_{epsilon}:_" +
                                  datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))
                prop_filename = (f"bounded_degree_k_colourability_tester_{size}_{epsilon}:_" +
                                 datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))

                graph_generator = GraphGenerator(False, self.directed, epsilon)

                k_col_testers = [lambda: BoundedDegreeGraphTester(graph_generator.generate_k_col_graph(size, k),
                                                                  epsilon).test_sparse_k_colourability(k)
                                 for _ in range(0, num_graphs_to_test)]
                print("All k-col graphs generated")
                k_col_test_description = (f"Bounded-degree K-colourability tester evaluation on {k}-colourable graph"
                                          f" of size {size} using epsilon {round(epsilon, 2)}\n")
                k_col_evaluator = Evaluator(prop_filename, k_col_testers, k_col_test_description,False)
                k_col_evaluator.test_method(num_iterations_per_graph)

                not_k_col_testers = [lambda: BoundedDegreeGraphTester(graph_generator
                                                                      .generate_e_far_from_k_col_graph(size, k),
                                                                      epsilon).test_sparse_k_colourability(k)
                                     for _ in range(0, num_graphs_to_test)]
                print("All e-far from k-col graphs generated")
                not_k_col_test_description = (f"Bounded-degree k-colourability tester evaluation on epsilon-far from "
                                              f"{k}-colourable graph of size {size} with epsilon {round(epsilon, 2)}\n")
                not_k_col_evaluator = Evaluator(e_far_filename, not_k_col_testers, not_k_col_test_description, True)
                not_k_col_evaluator.test_method(num_iterations_per_graph)

    def evaluate_bounded_degree_cycle_freeness_tester(self, num_iterations_per_graph, num_graphs_to_test):

        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                e_far_filename = (f"bounded_degree_cycle_freeness_tester_epsilon_far_{size}_{epsilon}:_" +
                                  datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))
                prop_filename = (f"bounded_degree_cycle_freeness_tester_{size}_{epsilon}:_" +
                                 datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))

                graph_generator = GraphGenerator(False, self.directed, epsilon)

                acyclic_testers = [BoundedDegreeGraphTester(graph_generator.generate_cycle_free_graph(size), epsilon)
                                  .test_cycle_freeness for _ in range(0, num_graphs_to_test)]
                acyclic_test_description = (f"Bounded-degree cycle freeness tester evaluation on cycle-free graph"
                                            f" of size {size} using epsilon {round(epsilon, 2)}\n")
                acyclic_evaluator = Evaluator(prop_filename, acyclic_testers, acyclic_test_description, False)
                acyclic_evaluator.test_method(num_iterations_per_graph)

                cyclic_testers = [BoundedDegreeGraphTester(graph_generator.generate_e_far_from_cycle_free_graph(size),
                                                           epsilon)
                                  .test_cycle_freeness for _ in range(0, num_graphs_to_test)]
                cyclic_test_description = (f"Bounded-degree cycle freeness tester evaluation on epsilon far from "
                                           f"cycle-free graph of size {size} with epsilon {round(epsilon, 2)}\n")
                acyclic_evaluator = Evaluator(e_far_filename, cyclic_testers, cyclic_test_description, True)
                acyclic_evaluator.test_method(num_iterations_per_graph)

    def evaluate_multiprocess_bounded_degree_cycle_freeness_tester(self, num_iterations_per_graph, num_graphs_to_test):

        for size in self.graph_sizes:
            for epsilon in self.epsilons:
                e_far_filename = (f"multiprocess_bounded_degree_cycle_freeness_tester_epsilon_far_{size}_{epsilon}:_" +
                                  datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))
                prop_filename = (f"multiprocess_bounded_degree_cycle_freeness_tester_{size}_{epsilon}:_" +
                                 datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))

                graph_generator = GraphGenerator(False, self.directed, epsilon)

                acyclic_testers = [BoundedDegreeGraphTester(graph_generator.generate_cycle_free_graph(size), epsilon)
                                  .multiprocess_test_cycle_freeness for _ in range(0, num_graphs_to_test)]
                acyclic_test_description = (f"Multiprocess bounded-degree cycle freeness tester evaluation on "
                                            f"cycle-free graph of size {size} using epsilon {round(epsilon, 2)}\n")
                acyclic_evaluator = Evaluator(prop_filename, acyclic_testers, acyclic_test_description, False)
                acyclic_evaluator.test_method(num_iterations_per_graph)

                cyclic_testers = [BoundedDegreeGraphTester(graph_generator.generate_e_far_from_cycle_free_graph(size),
                                                           epsilon)
                                  .multiprocess_test_cycle_freeness for _ in range(0, num_graphs_to_test)]
                cyclic_test_description = (f"Multiprocess bounded-degree cycle freeness tester evaluation on epsilon"
                                           f"far from cycle-free graph of size {size} "
                                           f"with epsilon {round(epsilon, 2)}\n")
                acyclic_evaluator = Evaluator(e_far_filename, cyclic_testers, cyclic_test_description, True)
                acyclic_evaluator.test_method(num_iterations_per_graph)
