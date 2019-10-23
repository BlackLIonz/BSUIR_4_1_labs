import os
from pathlib import Path


SOURCE_DIR = "/home/shota/projects/BSUIR_4_1_labs/SAIO/theory/"


def fix_folder(dir):
    for filename in os.listdir(dir):
        if filename.endswith(".JPG"):
            new_filename = filename.replace(".JPG", ".jpg")
            os.rename(
            os.path.join(dir, filename),
            os.path.join(dir, new_filename)
            )


def iterate_folder(dir):
    pathlist = Path(dir).glob('**/*.JPG')
    for path in pathlist:
        # because path is object not string
        path_in_str = '/'.join(str(path).split('/')[:-1])
        fix_folder(path_in_str)


if __name__ == '__main__':
    iterate_folder(SOURCE_DIR)
