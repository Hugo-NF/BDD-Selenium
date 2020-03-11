import os


def correct_file_extension(path, extension):
    split_path = os.path.splitext(path)
    if split_path[1] == extension:
        return path
    else:
        return path + extension
