import argparse

from config.ss_cleaner_cfg import TARGET_DIRPATH, COLLECTOR_DIRPATH, PATTERN
from utility import FileUtility, procedure, NextStep


def main():
    print("")
    print("------------------------------------------------------------")
    print("Screenshot Cleaner script")
    print("------------------------------------------------------------")

    init_check()


@procedure(show_time=False)
def init_check():
    FileUtility.check_dirpath_exists(TARGET_DIRPATH)
    parser = argparse.ArgumentParser()
    parser.add_argument("-nc", action="store_true", help="Skip confirm of the script")
    confirm_flag = False if parser.parse_args().nc is True else True
    if confirm_flag is True:
        return NextStep(confirm, {})
    else:
        return NextStep(check_collector_dir, {})


@procedure((
        f"Running Screenshot Cleaner script will collect all matched files according to the following configs:\n"
        f"* Target directory: {TARGET_DIRPATH}\n"
        f"* Collect directory: {COLLECTOR_DIRPATH}\n"
        f"* Regular expresion: {PATTERN}\n"
        "\n"
        f"Press [y/N] to proceed...\n"
),
    user_input=True,
    show_time=False)
def confirm(user_input):
    if user_input.lower().strip() != "y":
        print("ByeBye~")
        return NextStep(None, {})
    else:
        return NextStep(check_collector_dir, {})


@procedure("Checking collector directory", show_time=True)
def check_collector_dir():
    FileUtility.create_dirpath_if_not_exists(COLLECTOR_DIRPATH)
    return NextStep(move_files, {})


@procedure("Moving files", show_time=True)
def move_files():
    filepaths = []
    filepaths.extend(FileUtility.get_filepaths(TARGET_DIRPATH, pattern=PATTERN))
    for filepath in filepaths:
        FileUtility.move_file_to_dirpath(filepath, COLLECTOR_DIRPATH)
    context = {"filepaths": filepaths}
    return NextStep(print_report, context=context)


@procedure("Task complete!", show_time=False)
def print_report(filepaths):
    print(f"{len(filepaths)} screenshots have been collected")
    return NextStep(None, {})


if __name__ == "__main__":
    main()
