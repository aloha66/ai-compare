import os


def get_file_paths(data_folder):
    file_paths = []
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            yield os.path.join(root, file)


def load_text(path):
    with open(path,encoding="utf-8") as f:
        return f.read()