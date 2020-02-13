import os
import sys

exception_message = "dmesg_parser: exception"


def delete_timestamps(dmesg_output_file_name):
    if not os.path.isfile(dmesg_output_file_name):
        raise Exception(dmesg_output_file_name + " is not a file!")

    opened_file = open(dmesg_output_file_name, "r")
    dmesg_without_timestamps = []
    dmesg_with_timestamps = opened_file.readlines()

    for line in dmesg_with_timestamps:
        try:
            dmesg_without_timestamps.append(line.split("]", 1)[1][1:-1])
        except IndexError:
            dmesg_without_timestamps.append(exception_message)

    opened_file.close()
    return dmesg_without_timestamps


def is_excluded_line(line, excluded_patterns):
    for pattern in excluded_patterns:
        if pattern in line:
            return True

    return False


def straight_line_to_line_differences(text_list_1, text_list_2, excluded_patterns):
    min_text_list = text_list_1 if (len(text_list_1) < len(text_list_2)) else text_list_2
    max_text_list = text_list_1 if (len(text_list_1) > len(text_list_2)) else text_list_2

    different_lines = []
    idx = 0
    for line in min_text_list:
        if line != max_text_list[idx] and line != exception_message and not is_excluded_line(line, excluded_patterns):
            different_lines.append([str(idx + 1), line, max_text_list[idx]])
        idx = idx + 1

    start_pos = idx
    if len(max_text_list) > len(min_text_list):
        for line in max_text_list[start_pos:]:
            if line != exception_message and not is_excluded_line(line, excluded_patterns):
                different_lines.append([str(idx + 1), "", line])
            idx = idx + 1

    return different_lines


def random_line_to_line_differences(difference_list):
    processed_diff_list = []

    for elem_1 in difference_list:
        found = False
        for elem_2 in difference_list:
            if elem_1[1] == elem_2[2]:
                found = True
                break
        if not found:
            processed_diff_list.append(elem_1)

    return processed_diff_list


if len(sys.argv[1:]) < 2:
    raise Exception("You should enter at least 2 arguments!")

print("Deleting timestamps for " + sys.argv[1] + " ...")
parsed_dmesg_1 = delete_timestamps(sys.argv[1])
print("Timestamps are deleted!")

print("Deleting timestamps for " + sys.argv[2] + " ...")
parsed_dmesg_2 = delete_timestamps(sys.argv[2])
print("Timestamps are deleted!")

excluded_patterns_list = []
if len(sys.argv[1:]) == 3:
    if os.path.isfile(sys.argv[3]):
        exclude_file = open(sys.argv[3], "r")
        excluded_patterns_list = list(map(lambda s: s.strip(), exclude_file.readlines()))

print("Show differences in lines ...\n")
pre_process_list = straight_line_to_line_differences(parsed_dmesg_1, parsed_dmesg_2, excluded_patterns_list)
result_list = random_line_to_line_differences(pre_process_list)
for elem in result_list:
    print(elem[0] + ": \"" + elem[1] + "\" VS \"" + elem[2] + "\"")
