import os
import shutil
from pathlib import Path

from config.porter_cfg import DESTINATION_DIRPATH, TASKS
from utility import AutomationScript, FileUtility, print_proc_report


class PorterScript(AutomationScript):
    script_name: str = "Porter"
    confirm_flag: bool = True
    confirm_message: str = (
        "Running Porter script will copy the directories you assign and create a compressed file. \n"
        "(Check config file in the project for details)"
    )
    report_message: str = None

    COMPRESS_FORMAT = "zip"
    EXPORT_FILENAME = f"Porter {FileUtility.get_datetime_stamp()}.{COMPRESS_FORMAT}"

    def init_check(self):
        FileUtility.check_dirpath_exists(DESTINATION_DIRPATH)

    def body(self):
        # create staging dir
        staging_dirpath = None

        @print_proc_report("Creating staging directory")
        def proc():
            nonlocal staging_dirpath
            staging_dirpath = os.path.join(str(Path.home()), "backup_tmp")
            os.makedirs(staging_dirpath, exist_ok=False)

        proc()

        # collect dirs/files
        @print_proc_report("Collecting files")
        def proc():
            for task in TASKS:
                basename = os.path.basename(task.src_dirpath)
                shutil.copytree(task.src_dirpath, os.path.join(staging_dirpath, basename),
                                ignore=shutil.ignore_patterns(*task.ignore_patterns))

        proc()

        # zip
        zip_filepath = None

        @print_proc_report("zipping")
        def proc():
            nonlocal zip_filepath
            zip_filepath = shutil.make_archive(self.EXPORT_FILENAME, format=self.COMPRESS_FORMAT,
                                               root_dir=staging_dirpath)

        proc()

        # move zip file
        des_filepath = None

        @print_proc_report("Moving files")
        def proc():
            nonlocal des_filepath
            des_filepath = os.path.join(DESTINATION_DIRPATH, self.EXPORT_FILENAME)
            shutil.move(zip_filepath, des_filepath)

        proc()

        # remove staging directory
        @print_proc_report("Removing staging files")
        def proc():
            shutil.rmtree(staging_dirpath)

        proc()

        # report
        self.report_message = f"filepath: {des_filepath}"


if __name__ == "__main__":
    PorterScript().run()
