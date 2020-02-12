import os
import sys
import shutil


def check_and_delete(current_path, name_part, verbose):
    if current_path.find(name_part) != -1:
        print("------------------------------------------------------------------")
        if verbose:
            while True:
                print("ATTENTION! Delete path " + current_path + " ? [Y/N]: ")
                answer = input()
                if answer.lower() == "y":
                    print("Deleting path " + current_path + " ...")
                    if os.path.isfile(current_path):
                        os.remove(current_path)
                    else:
                        shutil.rmtree(current_path)
                    print("Path " + current_path + " is deleted!")
                    return True
                elif answer.lower() == "n":
                    print("Abort deleting path " + current_path + " !")
                    return True
        else:
            print("Deleting path " + current_path + " ...")
            if os.path.isfile(current_path):
                os.remove(current_path)
            else:
                shutil.rmtree(current_path)
            print("Path " + current_path + " is deleted!")
            return True
    else:
        if os.path.isfile(current_path):
            return True
        else:
            return False


def fs_tree_dfs(current_path, name_part, verbose):
    if not os.path.exists(current_path):
        print(current_path + " : no such file or directory!")
        return
    if not check_and_delete(current_path, name_part, verbose):
        with os.scandir(current_path) as entries:
            for sub_path in entries:
                fs_tree_dfs(current_path + os.sep + sub_path.name, name_part, verbose)


if len(sys.argv[1:]) < 3:
    print("usage: path_deleter [starting_path] [deleting_path_name_part] [v/s]")
    exit(-1)

silent = True if sys.argv[3].lower() == "s" else False
fs_tree_dfs(sys.argv[1], sys.argv[2], not silent)
