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
EMPTY_LINE = "(^\s$)|(^//)"
COMMENT = "//.*$"

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


# The main program:
if __name__ == "__main__":
    list_of_files_path = get_files(sys.argv)
    for file_path in list_of_files_path:
        assembly_lines_list = [] # some magic here...
        lines_list_to_file(file_output_path(file_path), assembly_lines_list)