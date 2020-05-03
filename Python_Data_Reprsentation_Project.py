"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

IDENTICAL = -1


def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
    """
    length_line1 = len(line1)
    length_line2 = len(line2)
    length_of_line = min(length_line1, length_line2)
    if length_of_line != 0:
        for length in range(length_of_line):
            if line1[length] == line2[length]:
                flag = 1
            else:
                flag = 0
                # found_index = line2.find(line2[length])
                found_index = length
                break
        if flag == 1:
            smaller_length = min(len(line1), len(line2))
            if smaller_length < length_line1 or smaller_length < length_line2:
                found_index = smaller_length
                return found_index
            else:
                # print(singleline_diff_format(line1, line2, IDENTICAL))
                return IDENTICAL
        else:
            # print(singleline_diff_format(line1, line2, found_index))
            return found_index
    else:
        smaller_length = min(len(line1), len(line2))
        greater_length = max(len(line1), len(line2))
        if smaller_length == 0 and greater_length != 0:
            found_index = length_of_line
            return found_index
        else:
            return IDENTICAL


def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
      :param line1:
      :param idx:
      :type line2: object
    """
    smaller_length = min(len(line1), len(line2))
    list1 = line1.split("\n")
    list2 = line2.split("\n")
    if len(list1) > 1 or len(list2) > 1 or idx == -1:
        return ""
    elif idx > smaller_length + 1 or idx < 0:
        return ""
    else:
        formatted_string = line1 + "\n" + "=" * idx + "^" + "\n" + line2 + "\n"
        return formatted_string


def multiline_diff(line1, line2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
      :param lines1:
      :param lines2:
      :return:
    """
    smaller_list = min(len(line1), len(line2))
    if len(line1) == len(line2):
        if smaller_list != 0:
            for element in range(smaller_list):
                first_difference = singleline_diff(line1[element], line2[element])
                if first_difference != -1:
                    return element, first_difference
                elif first_difference == -1 and element == smaller_list - 1:
                    return first_difference, first_difference
        else:
            return IDENTICAL, IDENTICAL
    else:
        if len(line1) < len(line2):
            return len(line1), 0
        else:
            return len(line2), 0


def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    file = open(filename, "r")
    data_in_file = file.read().splitlines()
    return data_in_file
    #file.close()


def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    filename1_list = get_file_lines(filename1)
    filename2_list = get_file_lines(filename2)
    difference = multiline_diff(filename1_list, filename2_list)
    print(difference)
    if difference[1] == -1:
        return "No differences\n"
    else:
        if len(filename1_list) == 0:
            first_line = "Line " + str(difference[0]) + ":\n"
            first_param = ""
            second_param = filename2_list[difference[0]]
            second_line = singleline_diff_format(first_param, second_param, difference[1])
            difference_string = first_line + second_line
            return difference_string

        elif len(filename2_list) == 0:
            first_line = "Line " + str(difference[0]) + ":\n"
            first_param = filename1_list[difference[0]]
            second_param = ""
            second_line = singleline_diff_format(first_param, second_param, difference[1])
            difference_string = first_line + second_line
            return difference_string
        else:
            first_line = "Line " + str(difference[0]) + ":\n"
            first_param = filename1_list[difference[0]]
            second_param = filename2_list[difference[0]]
            second_line = singleline_diff_format(first_param, second_param, difference[1])
            difference_string = first_line + second_line
            return difference_string


# LINE1 = "a"
# LINE2 = "b"
# print(multiline_diff(LINE1, LINE2))
# print(multiline_diff(['lines1', 'line2'], ['line1', 'line2']))
# print(multiline_diff([], []))
# singleline_diff_format(line1, line2, 2)

# print(singleline_diff('', ''))
#get_file_lines("data.txt")
#print(file_diff_format("file6.txt", "file7.txt"))
#print(file_diff_format('file1.txt', 'file9.txt'))
# print(singleline_diff_format("", "python", 0))