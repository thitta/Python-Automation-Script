import datetime
import os
import re
import shutil
from typing import List


class FileUtility:

    @staticmethod
    def check_dirpath_exists(dirpath):
        if os.path.isdir(dirpath) is False:
            msg = f"Directory {dirpath} is invalid."
            raise InvalidDirectoryError(msg)

    @staticmethod
    def copy_dirpaths(src_dirpaths, des_dirpath, ignore_patterns=None):
        for src_dirpath in src_dirpaths:
            basename = os.path.basename(src_dirpath)
            shutil.copytree(src_dirpath, os.path.join(des_dirpath, basename),
                            ignore=shutil.ignore_patterns(*ignore_patterns))

    @staticmethod
    def get_datetime_stamp():
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d at %H:%M:%S")
        return datetime_str

    @staticmethod
    def get_filepaths(dirpath: str, pattern="") -> List[str]:
        all_filenames = os.listdir(dirpath)
        rgex = re.compile(pattern)
        filtered_filenames = [filename for filename in all_filenames if rgex.match(filename) is not None]
        filtered_filepaths = [os.path.join(dirpath, filename) for filename in filtered_filenames]
        return filtered_filepaths

    @staticmethod
    def create_dirpath_if_not_exists(dirpath: str):
        os.makedirs(dirpath, exist_ok=True)

    @staticmethod
    def move_file_to_dirpath(src_filepath: str, dest_dirpath: str):
        basename = os.path.basename(src_filepath)
        dest_filepath = os.path.join(dest_dirpath, basename)
        shutil.move(src_filepath, dest_filepath)


class InvalidDirectoryError(Exception):
    pass
