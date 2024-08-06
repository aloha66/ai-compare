import os


def get_file_paths(data_folder):
    file_paths = []
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths


def load_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()
