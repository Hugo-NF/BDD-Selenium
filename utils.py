import os
from regexp import RegularExpressions
from re import sub, match


def correct_file_extension(path, extension):
    split_path = os.path.splitext(path)
    if split_path[1] == extension:
        return path
    else:
        return path + extension


def extract_path(full_path):
    return os.path.split(full_path)


def extract_filename(full_path):
    return os.path.basename(full_path)


def extract_module_name(full_path):
    filename = extract_filename(full_path)
    return os.path.splitext(filename)[0]


def get_value_or_default(dictionary, key, default_value):
    try:
        return dictionary[key]
    except KeyError:
        return default_value


def pre_process_file(file_path):
    with open(file_path, 'r', encoding='utf8') as fp:
        lines = fp.readlines()

        # Removing comments
        lines = list(map(lambda x: sub(RegularExpressions.regexps['comment'], '', x), lines))
        # Removing blank lines
        lines = list(filter(lambda x: not match(RegularExpressions.regexps['blank_line'], x), lines))
        # Removing line breaks
        lines = list(map(lambda x: sub(RegularExpressions.regexps['line_break'], '', x), lines))
        return lines
