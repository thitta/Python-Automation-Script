from utility import FileUtility
from utility.print_utility import *


class PorterTask:

    def __init__(self, src_dirpath: str, ignore_patterns: Iterable[str] = ()):
        FileUtility.check_dirpath_exists(src_dirpath)
        self.src_dirpath = src_dirpath
        self.ignore_patterns = ignore_patterns

    def __str__(self):
        return f"Target Directory: {self.src_dirpath}"
