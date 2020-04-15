from utils import pre_process_file
from regexp import RegularExpressions

import re


class Feature:

    def __init__(self, file_path):
        self.file_content = pre_process_file(file_path)
        self.process_file()

    def process_file(self):
        for line in self.file_content:
            match = re.match(RegularExpressions.regexps['statement'], line, re.IGNORECASE | re.MULTILINE)
            if match:
                groups = match.groups()
                indentation = groups[0]
                statement = groups[1]
                name = groups[2]
                print(indentation, statement, name)
