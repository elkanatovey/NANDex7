##############################################################################
# FILE : VMTranslatorpy
# WRITER : Aviad Dudkewitz, Elkana Tovey
# DESCRIPTION: This program translate VM code to Hack assembly language.
##############################################################################
import sys
import re
from pathlib import Path
from os import listdir


NUMBER_OF_ARGS = 2

INVALID_ARGS = "The file given as input is invalid..."
VALID_INPUT_SUFFIX = ".*\.vm$"
VM_SUFFIX = "\.vm$"
ASSEMBLY_SUFFIX = ".asm"
EMPTY_LINE = "^\s*$"
COMMENT = "//.*$"

ARITHMETIC_COMMAND = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or",
                      "not"]
MEMORY_ACCESS_COMMAND = ["push", "pop"]
PROGRAM_FLOW_COMMAND = ["label", "goto", "if-goto"]
FUNCTION_CALLING_COMMAND = ["function", "call", "return"]

vm_suffix_pattern = re.compile(VALID_INPUT_SUFFIX)


def get_files(args):
    """
    :param args: the arguments given to the program.
    :return: the list of paths to .vm files
    """
    list_of_files_path = []
    if len(args) == NUMBER_OF_ARGS:
##############################################################################
# FILE : VMTranslatorpy
# WRITER : Aviad Dudkewitz, Elkana Tovey
# DESCRIPTION: This program translate VM code to Hack assembly language.
##############################################################################
import sys
import re
from pathlib import Path
from os import listdir

NUMBER_OF_ARGS = 2

INVALID_ARGS = "The file given as input is invalid..."
VALID_INPUT_SUFFIX = ".*\.vm$"
VM_SUFFIX = "\.vm$"
ASSEMBLY_SUFFIX = ".asm"
EMPTY_LINE = "^\s*$"
COMMENT = "//.*$"

ARITHMETIC_COMMAND = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or",
                      "not"]
MEMORY_ACCESS_COMMAND = ["push", "pop"]
PROGRAM_FLOW_COMMAND = ["label", "goto", "if-goto"]
FUNCTION_CALLING_COMMAND = ["function", "call", "return"]
COMPARISON_JUMP_COMMAND = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}

vm_suffix_pattern = re.compile(VALID_INPUT_SUFFIX)


def get_files(args):
    """
    :param args: the arguments given to the program.
    :return: the list of paths to .vm files
    """
    list_of_files_path = []
    if len(args) == NUMBER_OF_ARGS:
        if Path(args[1]).is_file() and vm_suffix_pattern.match(args[1]):
            list_of_files_path.append(args[1])
        elif Path(args[1]).is_dir():
            for file in listdir(args[1]):
                if vm_suffix_pattern.match(file):
                    list_of_files_path.append(args[1] + "/" + file)
        return list_of_files_path
    else:
        print(INVALID_ARGS)
        exit()


def file_output_path(file_path):
    """
    :param file_path: The original file path
    :return: the path to the output file (.hack).
    """
    return re.sub(VM_SUFFIX, ASSEMBLY_SUFFIX, file_path)


def lines_list_to_file(file_path, lines_list):
    """
    :param file_path: path to the output file
    :param lines_list: a list of lines to save to the output file
    :return: None
    """
    with open(file_path, "w+") as output_file:
        for line in lines_list:
            output_file.write(line + "\n")


def file_to_assembly_lines(file_path):
    """
    Takes a vm file and translate all lines to Hack assembly language.
    :param file_path:  a string representing a the file path.
    :return: a list with all the translated lines.
    """
    result = []
    with open(file_path, "r") as input_file:
        comparison_counter = 0
        for line in input_file:
            line = re.sub(COMMENT, "", line)
            line_as_list = line.split()
            if len(line_as_list) > 0:
                print(line_as_list)  # for testing.
                if line_as_list[0] in ARITHMETIC_COMMAND:
                    temp_result, comparison_counter = \
                        get_arithmetic_command_lines(line_as_list[0],
                                                     comparison_counter)
                    result += temp_result
                elif line_as_list[0] in MEMORY_ACCESS_COMMAND:
                    result += get_memory_command_lines(line_as_list[0],
                                                       line_as_list[1],
                                                       line_as_list[2])
                elif line_as_list[0] in PROGRAM_FLOW_COMMAND:
                    pass  # for project 8
                elif line_as_list[0] in FUNCTION_CALLING_COMMAND:
                    pass  # for project 8
    return result


def get_arithmetic_command_lines(command, comparison_counter):
    if command == "add":
        return ["//add:",
                "@SP",
                "A = M - 1",
                "D = M",
                "@SP",
                "M = M - 1",
                "A = M - 1",
                "M = M + D"], comparison_counter
    if command == "sub":
        return ["//sub:",
                "@SP",
                "A = M - 1",
                "D = M",
                "@SP",
                "M = M - 1",
                "A = M - 1",
                "M = M - D"], comparison_counter
    if command == "neg":
        return ["//neg:",
                "@SP",
                "A = M - 1",
                "M = -M"], comparison_counter
    if command in COMPARISON_JUMP_COMMAND.keys():
        comparison_counter += 1
        return ["//" + command + ":",
                "@SP",
                "A = M - 1",
                "D = M // D=y",
                "@SP",
                "M = M - 1",
                "A = M - 1",
                "D = M - D // D=x-y",
                "@" + str(comparison_counter) + "COMPARISON",
                "D;" + COMPARISON_JUMP_COMMAND[command],
                "M = 0",
                "@" + str(comparison_counter) + "COMPARISON_END",
                "0;JMP",
                "(" + str(comparison_counter) + "COMPARISON)",
                "M = -1",
                "(" + str(comparison_counter) + "COMPARISON_END)"], \
               comparison_counter
    if command == "and":
        return ["//and:",
                "@SP",
                "A = M - 1",
                "D = M",
                "@SP",
                "M = M - 1",
                "A = M - 1",
                "M = D&M"], comparison_counter
    if command == "or":
        return ["//or:",
                "@SP",
                "A = M - 1",
                "D = M",
                "@SP",
                "M = M - 1",
                "A = M - 1",
                "M = D|M"], comparison_counter
    if command == "not":
        return ["//not:",
                "@SP",
                "A = M - 1",
                "M = !M"], comparison_counter


def get_memory_command_lines(command, segment, index):
    if command == "push":
        return []
    elif command == "pop":
        return []


# The main program:
if __name__ == "__main__":
    list_of_files_path = get_files(sys.argv)
    assembly_lines_list = []
    for file_path in list_of_files_path:
        assembly_lines_list = file_to_assembly_lines(file_path)
        lines_list_to_file(file_output_path(file_path), assembly_lines_list)
