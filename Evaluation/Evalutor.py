import datetime
import time


class Evaluator:
    def __init__(self, filename, testers_to_evaluate, test_description, epsilon_far):
        # tester_to_evaluate = some GraphTester.test_property method
        self.testers_to_evaluate = testers_to_evaluate
        self.epsilon_far = epsilon_far

        self.filename = filename
        self.file = open(filename, "w")
        self.file.write(test_description)
        print(filename)
        print(test_description)

    def test_method(self, num_iterations):
        # test the method on the graph, write runtime and result to self.file as a csv
        # then print statistics to stdout
        self.file.write(f"Num graphs tested: {len(self.testers_to_evaluate)}, "
                        f"Num iterations per graph: {num_iterations}\n")

        num_successes = 0
        runtime_total = 0
        for property_test in self.testers_to_evaluate:
            for _ in range(0, num_iterations):
                start_time = time.process_time()
                result = property_test()
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

        # create statistics, print them then save them to the test results file
        print("Statistics:")

        total_iterations = num_iterations * len(self.testers_to_evaluate)
        avg_runtime_string = f"Average runtime: {runtime_total / total_iterations}\n"
        print(avg_runtime_string)
        self.file.write(avg_runtime_string)

        success_rate_string = (f"Success rate: {num_successes} out of {total_iterations}, "
                               f"{round(num_successes * 100 / total_iterations, 2)}%\n")
        print(success_rate_string)
        self.file.write(success_rate_string)

        self.close_file()

    def close_file(self):
        self.file.close()
