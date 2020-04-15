from utils import pre_process_file


class Feature:

    def __init__(self, file_path):
        self.file_content = pre_process_file(file_path)

    def process_file(self):
        for line in self.file_content:
            print()