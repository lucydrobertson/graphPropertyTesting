from Evaluation.EvaluationHarness import EvaluationHarness
import math

if __name__ == "__main__":
    # generate a number of graphs of different sizes
    # then test it with a property tester
    # using the evaluation harness

    # problem: ran out of memory when trying to test on graphs of size 10000
    # epsilon values used: [1/20, 1/10, 1/6, 1/4, 1/3] [25, 100, 250, 1000]

    harness = EvaluationHarness([25, 100, 250, 1000], [1/20, 1/10, 1/6, 1/4, 1/3], False)

    # done: harness.evaluate_dense_bipartiteness_tester(3, 10)
    # done: harness.evaluate_dense_degree_regularity_tester(3, 10, 6)

    # come back to me: harness.evaluate_bounded_degree_bipartiteness_tester(3, 10)
    # done: harness.evaluate_bounded_degree_cycle_freeness_tester(3, 10)

    # will need to be different for k-col due to runtime, so just wait for now
    # can't evaluate dense k-col because its too slow (epsilon 1/3 on 1000 vertex graph has a 533 vertex subgraph)
    # can't evaluate bounded degree k-col because we need to work out the constants

    """
    # code to calculate how many vertices chosen for dense k-col subgraph tests
    k = 3
    for x in [1/20, 1/10, 1/6, 1/4, 1/3, 1/2]:
        print("Epsilon: ", x)
        num_select = int(k ** 2 * math.log(3 * k) / x ** 3)
        print("GGR: ", num_select)
        c = 2 * math.log(k)
        print("Alon: ", int(c * k * math.log(k) / x ** 2))
    exit(0)
    """

    # using epsilons [1/6, 1/4, 1/3]
    harness.evaluate_dense_k_colourability_tester(1, 1, 3)
    # harness.evaluate_bounded_degree_k_colourability_tester(1, 1, 3)
