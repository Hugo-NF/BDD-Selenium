"""BDD-Selenium - generators.py
This file contains the functions to write files to users desired output (e.g. file generation tool)
"""

import json
from utils import *


def generate_environment(full_path):
    """Dumps an example of an environment JSON file

    :param full_path: destination path
    :return: void
    """
    rev_path = correct_file_extension(full_path, '.json')
    path_only = extract_path(full_path)[0]
    with open(rev_path, 'w', encoding='utf-8') as fp:
        json.dump({
            "root_path": "https://your_website_root_path",
            "language": "en-US",
            "paths": {
                "features_path": path_only + '/features',
                "steps_path": path_only + '/steps',
                "factories_path": path_only + '/factories'
            }
        }, fp, indent=4)


""" Dictionary 'generator' maps the generator argument into the reference of the function """
generators = {
    'env': generate_environment
}
