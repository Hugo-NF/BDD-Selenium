import os


def correct_file_extension(path, extension):
    split_path = os.path.splitext(path)
    if split_path[1] == extension:
        return path
    else:
        return path + extension


def extract_path(full_path):
    return os.path.split(full_path)


def get_value_or_default(dictionary, key, default_value):
    try:
        return dictionary[key]
    except KeyError:
        return default_value
