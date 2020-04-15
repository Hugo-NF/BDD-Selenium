from regexp import RegularExpressions
from re import match, RegexFlag

class Feature:

    def __init__(self, file_path):
        self.file_content = self.pre_process_file(file_path)

    def pre_process_file(self, file_path):
        with open(file_path, 'r', encoding='utf8') as fp:
            lines = fp.readlines()
            for line in lines:
                if RegularExpressions.regexps['blank_line'].match(line):
                    lines.remove(line)
                elif RegularExpressions.regexps['comment'].match(line):
                    lines.remove(line)

            print(lines)