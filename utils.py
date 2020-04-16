"""BDD-Selenium - utils.py
This file contains helper methods that do not depend on the application context
and it's perfectly reusable in other projects
"""


import os
from re import sub, match
from definitions import *


def correct_file_extension(path, extension):
    """Insert the desired file extension (or replace the current) on the file path

    :param path: the path of the file (either absolute or relative)
    :param extension: the desired extension for the file
    :return: the path string containing the request extension
    """
    split_path = os.path.splitext(path)
    if split_path[1] == extension:
        return path
    else:
        return path + extension


def extract_path(full_path):
    """Splits the argument between path and filename

    :param full_path: complete file path string
    :return: tuple containing (path, filename), remains empty if not present in full_path
    """
    return os.path.split(full_path)


def extract_filename(full_path):
    """Remove and return filename (with extension) from file_path

    :param full_path: complete file path string
    :return: tuple containing (path, filename), remains empty if not present in full_path
    """
    return os.path.basename(full_path)


def extract_module_name(full_path):
    """Extract module name following the Python's PEP 8 convention

    :param full_path: complete file path string
    :return: module_name (filename without extension)
    """
    filename = extract_filename(full_path)
    return os.path.splitext(filename)[0]


def check_indentation(indent_obj):
    """Tests (True or False) if the indentation is correct for that line

    :param indent_obj: tuple with following fields (amount of indents in line, file tab size, expected amount of indents)
    :return: True if indentation correct, False otherwise
    """
    return indent_obj[0] == (indent_obj[1] * indent_obj[2])


def get_value_or_default(dictionary, key, default_value):
    """Get an value from dictionary, if not exists, returns the default value

    :param dictionary: queried dictionary
    :param key: requested key
    :param default_value: default value for that key
    :return: value present in the dictionary (default_value otherwise)
    """

    try:
        return dictionary[key]
    except KeyError:
        return default_value


def pre_process_file(file_path):
    """Executes the pre-processing task on a given file
    Opens the file with (file_path) filename and removes:
        Empty lines,
        single line comments with #

    :param file_path: address of the file to be processed
    :return: list of processed lines
    """
    with open(file_path, 'r', encoding='utf8') as fp:
        lines = fp.readlines()

        # Removing comments
        lines = list(map(lambda x: sub(RegularExpressions.regexps['comment'], '', x), lines))
        # Removing blank lines
        lines = list(filter(lambda x: not match(RegularExpressions.regexps['blank_line'], x), lines))
        # Removing line breaks
        lines = list(map(lambda x: sub(RegularExpressions.regexps['line_break'], '', x), lines))
        return lines
