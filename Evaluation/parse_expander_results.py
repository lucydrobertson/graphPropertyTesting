import math
from lib2to3.fixes.fix_tuple_params import tuple_name
from os import listdir
from os.path import isfile, join
from statistics import mean, stdev


def get_filenames(folder):
    dirpath = "/home/lucy/Desktop/University/graphPropertyTesting/Evaluation/Final Results/"
    mypath = dirpath + folder
    only_files = [mypath + f for f in listdir(mypath) if isfile(join(mypath, f))]
    return only_files


def calculate_confidence_interval(results):
    # calculate a 95% confidence interval for these results
    results_mean = mean(results)
    results_stdev = stdev(results)

    # z-value for a 95% confidence interval is 1.96
    z = 1.96
    # formula: mean +- z * stdev / sqrt(n) where n is the number of results
    difference = z * results_stdev / math.sqrt(len(results))
    return difference


def get_stats_from_file(filename):
    f = open(filename, "r")
    lines = f.read().split("\n")
    f.close()

    # get alpha and epsilon values, and if graph has property or is e-far
    line1_tokens = lines[0].split(" ")
    alpha = filename.split("_")[-2]
    epsilon = 0
    has_property = True

    for i in range(0, len(line1_tokens)):
        if line1_tokens[i] == "epsilon":
            epsilon = line1_tokens[i + 1]

    results = []
    for result_line in lines[2:-3]:
        results.append(float(result_line.split(",")[0]))

    confidence_interval = calculate_confidence_interval(results)

    # get average runtime and success rate
    runtime_line = lines[-3]
    runtime = runtime_line.split(": ")[1]

    success_rate_line = lines[-2]
    success_rate = success_rate_line.split(", ")[1][:-1]

    stats_line = f"{alpha},{epsilon},{runtime},{confidence_interval},{success_rate},{has_property}\n"
    return stats_line


def get_all_stats(filenames, results_filename):
    results = [get_stats_from_file(f) for f in filenames]
    r_file = open(results_filename, "w")
    r_file.write("alpha,epsilon,average_runtime,average_runtime_confidence,success_rate,has_property\n")
    for r in results:
        r_file.write(r)
    r_file.close()


if __name__ == "__main__":
    folder_name = "Expander_Tester/"
    results_filename = "Expander_results.csv"

    files = get_filenames(folder_name)
    get_all_stats(files, results_filename)

