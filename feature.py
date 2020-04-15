from utils import pre_process_file
from regexp import RegularExpressions

import re


class Feature:

    def __init__(self, file_path, steps, env_variables, locale):
        self.file_content = pre_process_file(file_path)
        self.process_file(steps, env_variables, locale)

    def process_file(self, steps, env_variables, locale):
        for line in self.file_content:
            match = re.match(RegularExpressions.regexps['statement'], line, re.IGNORECASE | re.MULTILINE)
            if match:
                groups = match.groups()
                indentation = groups[0]
                statement = groups[1]
                name = groups[2]
                statement = statement.lower()
                print(indentation, statement, name)
