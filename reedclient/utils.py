from os import path


def read_file(file_name):
    with open(path.expanduser("~/") + file_name) as f:
        return f.read().strip("\n")
