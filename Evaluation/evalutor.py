import datetime
import time


class Evaluator:
    def __init__(self, tester_to_evaluate, test_description, epsilon_far):
        # tester_to_evaluate = some GraphTester.test_property method
        self.tester_to_evaluate = tester_to_evaluate
        self.epsilon_far = epsilon_far

        if self.epsilon_far:
            filename = (tester_to_evaluate.__name__ + "_epsilon-far" + ":_" +
                        datetime.datetime.now().strftime('%Y-%m-%d_%H:%M'))
        else:
            filename = tester_to_evaluate.__name__ + ":_" + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')

        print(filename)
        print(test_description)
        self.file = open(filename, "w")
        self.file.write(test_description)

    def test_method(self, num_iterations):
        # test the method on the graph, write runtime and result to self.file as a csv
        # then print statistics to stdout
        num_successes = 0
        runtime_total = 0
        for _ in range(0, num_iterations):
            start_time = time.process_time()
            result = self.tester_to_evaluate()
            end_time = time.process_time()
            run_time = end_time - start_time

            runtime_total += run_time
            if result and not self.epsilon_far:
                num_successes += 1
            # if result == False and epsilon_far == True then we have a success because we are using the tester
            # on a graph that is epsilon far from having the property so it has correctly determined the result
            elif not result and self.epsilon_far:
                num_successes += 1

            # write out run to file
            self.file.write(f"{run_time},{result}\n")

        print("Statistics:")
        print(f"Number of iterations: {num_iterations}")
        print(f"Average runtime: {runtime_total / num_iterations}")
        print(f"Success rate: {num_successes} out of {num_iterations}, "
              f"{round(num_successes * 100 / num_iterations, 2)}%\n")

        self.close_file()

    def close_file(self):
        self.file.close()
