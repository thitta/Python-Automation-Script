from config.ss_cleaner_cfg import TARGET_DIRPATH, COLLECTOR_DIRPATH, PATTERN
from utility import FileUtility, AutomationScript, print_proc_report


class SsCleanerScript(AutomationScript):
    script_name: str = "Screenshot Cleaner"
    confirm_message: str = (
        f"Running Screenshot Cleaner script will collect all matched files according to the following configs:\n"
        f"* Target directory: {TARGET_DIRPATH}\n"
        f"* Collect directory: {COLLECTOR_DIRPATH}\n"
        f"* Regular expresion: {PATTERN}"
    )
    confirm_flag: bool = True
    report_message: str = None

    def init_check(self):
        FileUtility.check_dirpath_exists(TARGET_DIRPATH)

    def body(self):
        # check collector directory
        @print_proc_report("Checking collector directory")
        def proc():
            FileUtility.create_dirpath_if_not_exists(COLLECTOR_DIRPATH)

        proc()

        # move files
        filepaths = []

        @print_proc_report("Moving files")
        def proc():
            filepaths.extend(FileUtility.get_filepaths(TARGET_DIRPATH, pattern=PATTERN))
            for filepath in filepaths:
                FileUtility.move_file_to_dirpath(filepath, COLLECTOR_DIRPATH)

        proc()

        # report
        self.report_message = f"{len(filepaths)} screenshots have been collected"


if __name__ == "__main__":
    SsCleanerScript().run()
