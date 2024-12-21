from Evaluation.EvaluationHarness import EvaluationHarness

if __name__ == "__main__":
    # generate graph
    # then test it 100 times with a property tester
    # using the evaluation harness

    harness = EvaluationHarness([100], [1/8], False)
    harness.evaluate_dense_bipartiteness_tester(100)


