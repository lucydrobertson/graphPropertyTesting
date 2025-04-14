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

    # get size and epsilon values, and if graph has property or is e-far
    line1_tokens = lines[0].split(" ")
    size = 0
    epsilon = 0
    has_property = True

    for i in range(0, len(line1_tokens)):
        if line1_tokens[i] == "size":
            size = line1_tokens[i + 1]
        elif line1_tokens[i] == "epsilon":
            if line1_tokens[i + 1] == "far":
                has_property = False
            else:
                epsilon = line1_tokens[i + 1]
        elif line1_tokens[i] == "epsilon-far":
            has_property = False
        elif line1_tokens[i] == "epsilonfar":
            has_property = False

    results = []
    for result_line in lines[2:-3]:
        results.append(float(result_line.split(",")[0]))

    confidence_interval = calculate_confidence_interval(results)

    # get average runtime and success rate
    runtime_line = lines[-3]
    runtime = runtime_line.split(": ")[1]

    success_rate_line = lines[-2]
    success_rate = success_rate_line.split(", ")[1][:-1]

    stats_line = f"{size},{epsilon},{runtime},{confidence_interval},{success_rate},{has_property}\n"
    return stats_line


def get_all_stats(filenames, results_filename):
    results = [get_stats_from_file(f) for f in filenames]
    r_file = open(results_filename, "w")
    r_file.write("size,epsilon,average_runtime,average_runtime_confidence,success_rate,has_property\n")
    for r in results:
        r_file.write(r)
    r_file.close()


if __name__ == "__main__":
    tester_filename_pairs = [("BoundedDegree_Bipartiteness_Tester/", "BD_BPT_results.csv"),
                             ("BoundedDegree_Cycle_Freeness_Tester/", "BD_CycleFreeness_results.csv"),
                             ("BoundedDegree_kcol_Tester/", "BD_K-col_results.csv"),
                             ("Dense_Bipartiteness_Tester/", "Dense_BPT_results.csv"),
                             ("Dense_kcol_Tester/", "Dense_K-col_results.csv"),
                             ("Dense_Regularity_Tester/", "Dense_regular_results.csv"),
                             ("Multiprocess_BoundedDegree_Bipartiteness_Tester/", "MP_BD_BPT_results.csv"),
                             ("Multiprocess_BoundedDegree_Cycle_Freeness_Tester/", "MP_BD_CycleFreeness_results.csv")]

    results_path = "/Evaluation/"

    for (folder_name, results_filename) in tester_filename_pairs:
        files = get_filenames(folder_name)
        get_all_stats(files, results_path + results_filename)

