from Evaluation.EvaluationHarness import EvaluationHarness

if __name__ == "__main__":
    # generate graph
    # then test it 100 times with a property tester
    # using the evaluation harness
    harness = EvaluationHarness([1000], [1/10], False)
    harness.evaluate_dense_bipartiteness_tester(3, 10)

    # can't evaluate dense k-col because its too slow (epsilon 1/3 on 1000 vertex graph has a 533 vertex subgraph)
    # can't evaluate bounded degree k-col because we need to work out the constants

    """
    harness = EvaluationHarness([10, 25, 100, 250, 1000], [1/10, 1/6, 1/4, 1/3, 1/2], False)
    harness.evaluate_dense_bipartiteness_tester(100)
    harness.evaluate_dense_k_colourability_tester(100, 3)
    harness.evaluate_dense_degree_regularity_tester(100, 10)
    harness.evaluate_bounded_degree_bipartiteness_tester(100)
    harness.evaluate_bounded_degree_k_colourability_tester(100, 3)
    harness.evaluate_bounded_degree_cycle_freeness_tester(100)
    """