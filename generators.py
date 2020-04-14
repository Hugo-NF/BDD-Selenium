import json
from utils import *


def generate_environment(full_path):
    rev_path = correct_file_extension(full_path, '.json')
    path_only = extract_path(full_path)[0]
    with open(rev_path, 'w', encoding='utf-8') as fp:
        json.dump({
            "root_path": "https://your_website_root_path",
            "language": "en-US",
            "paths": {
                "features_path": path_only + '/features',
                "steps_path": path_only + '/steps',
                "scenarios_path": path_only + '/scenarios'
            }
        }, fp, indent=4)


generators = {
    'ENV': generate_environment
}
