from lib2to3.fixes.fix_tuple_params import tuple_name
from os import listdir
from os.path import isfile, join


def get_filenames(folder):
    dirpath = "/home/lucy/Desktop/University/graphPropertyTesting/Evaluation/Final Results/"
    mypath = dirpath + folder
    only_files = [mypath + f for f in listdir(mypath) if isfile(join(mypath, f))]
    return only_files


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

    # get average runtime and success rate
    runtime_line = lines[-3]
    runtime = runtime_line.split(": ")[1]

    success_rate_line = lines[-2]
    success_rate = success_rate_line.split(", ")[1][:-1]

    stats_line = f"{size},{epsilon},{runtime},{success_rate},{has_property}\n"
    return stats_line


def get_all_stats(filenames, results_filename):
    results = [get_stats_from_file(f) for f in filenames]
    r_file = open(results_filename, "w")
    r_file.write("size, epsilon, average_runtime, success_rate, has_property\n")
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

    results_path = "/home/lucy/Desktop/University/graphPropertyTesting/Evaluation/"

    for (folder_name, results_filename) in tester_filename_pairs:
        files = get_filenames(folder_name)
        get_all_stats(files, results_path + results_filename)

