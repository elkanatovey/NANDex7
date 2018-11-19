##############################################################################
# FILE : VMTranslatorpy
# WRITER : Aviad Dudkewitz, Alkana Tovey
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
DIRECTORY_NAME = "\\\.*$"
EMPTY_LINE = "^\s*$"
COMMENT = "//.*$"

ARITHMETIC_COMMAND = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or",
                      "not"]
MEMORY_ACCESS_COMMAND = ["push", "pop"]
PROGRAM_FLOW_COMMAND = ["label", "goto", "if-goto"]
FUNCTION_CALLING_COMMAND = ["function", "call", "return"]

vm_suffix_pattern = re.compile(VALID_INPUT_SUFFIX)
directory_pattern = re.compile(DIRECTORY_NAME)

VALID_INPUT_SUFFIX = ".*\.vm$"
COMPARISON_JUMP_COMMAND = {"gt": "JGT", "lt": "JLT", "eq": "JEQ"}
COMPARISON_X_GT_Y = {"gt": "-1", "lt": "0"}
COMPARISON_Y_GT_X = {"gt": "0", "lt": "-1"}
INCREMENT_STACK = ["@SP", "M = M + 1"]
DECREMENT_STACK = ["@SP", "M=M-1"]
FINISH_LOCATION_ADVANCE = ["D=M+D", "A=D", "D=M"]
FINISH_STACK_SET = ["@SP", "A=M", "M=D"]

comparison_counter = 0


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
    if Path(file_path).is_file():
        return re.sub(VM_SUFFIX, ASSEMBLY_SUFFIX, file_path)
    else:
        temp_list = file_path.split("/")
        return file_path +"/"+ temp_list[len(temp_list) - 1] + ASSEMBLY_SUFFIX


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
        for line in input_file:
            line = re.sub(COMMENT, "", line)
            line_as_list = line.split()
            if len(line_as_list) > 0:
                print(line_as_list)  # for testing.
                if line_as_list[0] in ARITHMETIC_COMMAND:
                    temp_result = get_arithmetic_command_lines(line_as_list[0])
                    result += temp_result
                elif line_as_list[0] in MEMORY_ACCESS_COMMAND:
                    result += get_memory_command_lines(line_as_list[0],
                                                       line_as_list[1],
                                                       line_as_list[2],
                                                       file_path)
                elif line_as_list[0] in PROGRAM_FLOW_COMMAND:
                    pass  # for project 8
                elif line_as_list[0] in FUNCTION_CALLING_COMMAND:
                    pass  # for project 8
    return result


def get_arithmetic_command_lines(command):
    """
    :param command: arithmetic vm command
    :return: Hack assembly language equivalent.
    """
    if command == "add":
        return ["//add:",
                "@SP",
                "A = M - 1",
                "D = M",
                "@SP",
                "M = M - 1",
                "A = M - 1",
                "M = M + D"]
    if command == "sub":
        return ["//sub:",
                "@SP",
                "A = M - 1",
                "D = M",
                "@SP",
                "M = M - 1",
                "A = M - 1",
                "M = M - D"]
    if command == "neg":
        return ["//neg:",
                "@SP",
                "A = M - 1",
                "M = -M"]
    if command in COMPARISON_JUMP_COMMAND.keys():
        global comparison_counter
        comparison_counter += 1
        if command == "eq":
            return ["//eq:",
                    "@SP",
                    "A = M - 1",
                    "D = M // D=y",
                    "@SP",
                    "M = M - 1",
                    "A = M - 1",
                    "D = M - D // D=x-y",
                    "@" + str(comparison_counter) + "COMPARISON_TRUE",
                    "D;JEQ",
                    "M = 0 // false",
                    "@" + str(comparison_counter) + "COMPARISON_END",
                    "0;JMP",
                    "(" + str(comparison_counter) + "COMPARISON_TRUE)",
                    "M = -1 // true",
                    "(" + str(comparison_counter) + "COMPARISON_END)"]
        else:
            return ["//" + command + ":",
                    "@SP",
                    "A = M - 1",
                    "D = M // D=y",
                    "@" + str(comparison_counter) + "COMPARISON_YGT0",
                    "D;JGE // if y>=0",
                    "//y<0",
                    "@SP",
                    "M = M - 1",
                    "A = M - 1",
                    "@" + str(comparison_counter) + "COMPARISON_SAME_SYMBOL",
                    "M;JLT // if x<0",
                    "//y<0, x>=0",
                    "M =" + COMPARISON_X_GT_Y[command],
                    "@" + str(comparison_counter) + "COMPARISON_END",
                    "0;JMP",
                    "(" + str(comparison_counter) + "COMPARISON_YGT0)",
                    "//y>=0",
                    "@SP",
                    "M = M - 1",
                    "A = M - 1",
                    "@" + str(comparison_counter) + "COMPARISON_SAME_SYMBOL",
                    "M;JGE // if x>=0",
                    "//y>=0, x<0",
                    "M =" + COMPARISON_Y_GT_X[command],
                    "@" + str(comparison_counter) + "COMPARISON_END",
                    "0;JMP",
                    "(" + str(comparison_counter) + "COMPARISON_SAME_SYMBOL)",
                    "D = M - D // D=x-y"
                    "@" + str(comparison_counter) + "COMPARISON_TRUE",
                    "D;" + COMPARISON_JUMP_COMMAND[command],
                    "M = 0 // false",
                    "@" + str(comparison_counter) + "COMPARISON_END",
                    "0;JMP",
                    "(" + str(comparison_counter) + "COMPARISON_TRUE)",
                    "M = -1 // true",
                    "(" + str(comparison_counter) + "COMPARISON_END)"]
    if command == "and":
        return ["//and:",
                "@SP",
                "A = M - 1",
                "D = M",
                "@SP",
                "M = M - 1",
                "A = M - 1",
                "M = D&M"]
    if command == "or":
        return ["//or:",
                "@SP",
                "A = M - 1",
                "D = M",
                "@SP",
                "M = M - 1",
                "A = M - 1",
                "M = D|M"]
    if command == "not":
        return ["//not:",
                "@SP",
                "A = M - 1",
                "M = !M"]


def realign_memory_pointer(index):
    pointer_alignment = ["@"+index, "D=A"]
    return pointer_alignment


def push_cases(segment, index, file_name):
    instructions_to_add = realign_memory_pointer(index)
    segment_type = ""
    if segment == "argument":
        segment_type = "@ARG"
    elif segment == "local":
        segment_type = "@LCL"
    elif segment == "static":
        file_name = file_name.replace(".vm", "." + index)
        name = file_name.split("/")
        file_name = "@"+name[len(name)-1]
        instructions_to_add = [file_name] + ["D=M"] + FINISH_STACK_SET + \
                              INCREMENT_STACK
        return instructions_to_add
    elif segment == "this":
        segment_type = "@THIS"
    elif segment == "that":
        segment_type = "@THAT"
    elif segment == "constant":
        instructions_to_add[1] = "D=A"
        instructions_to_add = instructions_to_add + FINISH_STACK_SET \
                              + INCREMENT_STACK
        return instructions_to_add
    elif segment == "pointer":
        segment_type = "@THAT"
        if index == '0':
            segment_type = "@THIS"
        instructions_to_add = [segment_type, "D=M", "@SP", "A=M", "M=D"] +\
                                  INCREMENT_STACK
        return instructions_to_add
    elif segment == "temp":
        segment_type = "@R5"
        instructions_to_add = instructions_to_add + [segment_type,"D=A+D",
                                                     "A=D", "D=M"] + \
                              FINISH_STACK_SET + INCREMENT_STACK
        return instructions_to_add
    instructions_to_add = instructions_to_add + [segment_type] +\
                        FINISH_LOCATION_ADVANCE + FINISH_STACK_SET +\
                          INCREMENT_STACK
    return instructions_to_add


def direct_mappings(index, map_type):
    index_point = realign_memory_pointer(index)
    mapped_list = ["@R15", "M=D"] + index_point + [map_type] + ["D=M+D",
                "@R14", "M=D", "@R15", "D=M", "@R14", "A=M", "M=D"]
    return mapped_list


def pop_cases(segment, index, file_name):
    return_list = DECREMENT_STACK + ["A=M", "D=M"]
    if segment == "argument":
        return_list = return_list + direct_mappings(index, "@ARG")
        return return_list
    elif segment == "local":
        return_list = return_list + direct_mappings(index, "@LCL")
        return return_list
    elif segment == "static":
        file_name = file_name.replace(".vm", "." + index)
        name = file_name.split("/")
        file_name = "@"+name[len(name)-1]
        return_list = return_list + file_name + ["M=D"]
        return return_list
    elif segment == "this":
        return_list = return_list + direct_mappings(index, "@THIS")
        return return_list
    elif segment == "that":
        return_list = return_list + direct_mappings(index, "@THAT")
        return return_list
    elif segment == "pointer":
        segment_type = "@THAT"
        if index == '0':
            segment_type = "@THIS"
        return_list = return_list + [segment_type, "M=D"]
        return return_list
    elif segment == "temp":
        segment_type = "@R5"
        index_to_add = realign_memory_pointer(index)
        return_list = return_list + ["@R15", "M=D"]+index_to_add +[
            segment_type, "D=D+A", "@R14", "M=D", "@R15", "D=M", "@R14",
            "A=M", "M=D"]
        return return_list


def get_memory_command_lines(command, segment, index, file_name):
    if command == "push":
        return push_cases(segment, index, file_name)
    elif command == "pop":
        return pop_cases(segment, index, file_name)


# The main program:
if __name__ == "__main__":
    comparison_counter = 0
    list_of_files_path = get_files(sys.argv)
    assembly_lines_list = []
    for file_path in list_of_files_path:
        assembly_lines_list += file_to_assembly_lines(file_path)
    lines_list_to_file(file_output_path(sys.argv[1]), assembly_lines_list)