import collections

from utility import FileUtility

COMPRESS_FORMAT = "zip"

EXPORT_FILENAME = f"Porter {FileUtility.get_datetime_stamp()}.{COMPRESS_FORMAT}"

DESTINATION_DIRPATH = "[the destination directory you wish to put your zip file in]"

PorterTask = collections.namedtuple("PorterTasks", ("src_dirpath", "ignore_patterns"))

TASKS = (
    # PorterTask("[source directory], [Iterable of strings, the pattern you wish to ignore]"),
)
