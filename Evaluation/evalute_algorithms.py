from Evaluation.EvaluationHarness import EvaluationHarness
import math


# code to calculate how many vertices chosen for dense k-col subgraph tests
def calc_k_col_subgraph_size():
    k = 3
    for x in [0.6, 0.7, 0.8, 0.9]:
        print("Epsilon: ", x)
        num_select = int(k ** 2 * math.log(3 * k) / x ** 3)
        print("GGR: ", num_select)
        c = 2 * math.log(k)
        print("Alon: ", int(c * k * math.log(k) / x ** 2))


if __name__ == "__main__":
    # generate a number of graphs of different sizes
    # then test it with a property tester
    # using the evaluation harness

    # problem: ran out of memory when trying to test on graphs of size 10000
    # epsilon values used: [1/20, 1/10, 1/6, 1/4, 1/3] [25, 100, 250, 1000]

    harness = EvaluationHarness([25, 100, 250, 1000], [1/20, 1/10, 1/6, 1/4, 1/3], False)
    
    harness.evaluate_dense_bipartiteness_tester(3, 10)
    harness.evaluate_dense_degree_regularity_tester(3, 10, 6)
    harness.evaluate_bounded_degree_cycle_freeness_tester(3, 10)
    harness.evaluate_multiprocess_bounded_degree_cycle_freeness_tester(3, 10)
    harness.evaluate_bounded_degree_bipartiteness_tester(3, 10)
    harness.evaluate_multiprocess_bounded_degree_bipartiteness_tester(3, 10)

    # size: [25, 100, 250, 1000], epsilon: [0.6, 0.7, 0.8, 0.9]
    k_col_harness = EvaluationHarness([100, 250, 1000], [0.6, 0.7, 0.8, 0.9], False)
    k_col_harness.evaluate_dense_k_colourability_tester(3, 10, 3)
    k_col_harness.evaluate_bounded_degree_k_colourability_tester(3, 10, 3)
