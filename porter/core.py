import argparse
import os
import shutil
from pathlib import Path

from config.porter_cfg import COMPRESS_FORMAT, EXPORT_FILENAME, DESTINATION_DIRPATH, TASKS
from utility import FileUtility, procedure, NextStep, teardown


def main():
    print("")
    print("------------------------------------------------------------")
    print("Porter script")
    print("------------------------------------------------------------")

    init_check()


@procedure()
def init_check():
    FileUtility.check_dirpath_exists(DESTINATION_DIRPATH)
    parser = argparse.ArgumentParser()
    parser.add_argument("-nc", action="store_true", help="Skip confirm of the script")
    confirm_flag = False if parser.parse_args().nc is True else True
    if confirm_flag is True:
        return NextStep(confirm, {})
    else:
        return NextStep(create_staging_dir, {})


@procedure((
        "Running Porter script will copy target directories and make a compress file to destination. \n"
        "(Check config file in the project for details)\n"
        "\n"
        "Press [y/N] to proceed...\n"),
    user_input=True,
)
def confirm(user_input):
    if user_input.lower().strip() != "y":
        print("ByeBye~")
        return NextStep(None, {})
    else:
        return NextStep(create_staging_dir, {})


@procedure("Creating staging directory...", show_time=True)
def create_staging_dir():
    staging_dirpath = os.path.join(str(Path.home()), "backup_tmp")
    os.makedirs(staging_dirpath, exist_ok=False)
    context = dict()
    context["staging_dirpath"] = staging_dirpath
    return NextStep(collect_files, context=context)


@procedure("Collecting files...", show_time=True)
def collect_files(staging_dirpath):
    for task in TASKS:
        basename = os.path.basename(task.src_dirpath)
        shutil.copytree(task.src_dirpath, os.path.join(staging_dirpath, basename),
                        ignore=shutil.ignore_patterns(*task.ignore_patterns))
    return NextStep(zip_files, {})


@procedure("Zipping files...", show_time=True)
def zip_files(staging_dirpath):
    zip_filepath = shutil.make_archive(EXPORT_FILENAME, format=COMPRESS_FORMAT,
                                       root_dir=staging_dirpath)
    context = dict()
    context["zip_filepath"] = zip_filepath
    return NextStep(move_zip_file_to_dest, context=context)


@procedure("Moving files...", show_time=True)
def move_zip_file_to_dest(zip_filepath):
    des_filepath = os.path.join(DESTINATION_DIRPATH, EXPORT_FILENAME)
    context = dict()
    context["des_filepath"] = des_filepath
    shutil.move(zip_filepath, des_filepath)
    return NextStep(print_report, context=context)


@procedure("Task complete!", show_time=False)
def print_report(des_filepath):
    msg = f"filepath: {des_filepath}"
    print(msg)
    return NextStep(None, {})


@teardown
def remove_staging_files(staging_dirpath):
    shutil.rmtree(staging_dirpath)
    return NextStep(print_report, {})


if __name__ == "__main__":
    main()
