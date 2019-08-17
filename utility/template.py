import argparse
import functools
import sys
import time
from builtins import NotImplementedError

from utility.print_utility import *


class AutomationScript:
    script_name: str = "Undefined script"
    confirm_message: str = "Empty confirm message"
    confirm_flag: bool = True
    report_message: str = None

    def init_check(self):
        raise NotImplementedError()

    def body(self):
        raise NotImplementedError()

    def run(self):

        # implement -nc option
        self._set_confirm_flag_by_args()

        # execute init check
        self.init_check()

        # print init message
        print_init_message(self.script_name)

        # execute confirm if necessary
        if self.confirm_flag is True:
            self._confirm()

        # execute body
        self.body()

        # end message
        print_end_message(self.script_name)

        # print report message if necessary
        if self.report_message is not None:
            print(self.report_message)
        print_newline()

    def disable_confirm(self):
        self.confirm_flag = False
        return self

    def _confirm(self):
        print(self.confirm_message)
        print_newline()
        option_msg = "Press [y/N] to proceed..."
        if input(option_msg).lower().strip() != "y":
            print("ByeBye~")
            sys.exit()
        print_newline()

    def _set_confirm_flag_by_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-nc", action="store_true", help="Skip confirm of the script")
        self.confirm_flag = False if parser.parse_args().nc is True else self.confirm_flag


def print_proc_report(proc_description):
    def arg_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{proc_description}......")
            now = time.time()
            func(*args, **kwargs)
            print(f"ok({round(time.time() - now, 2)} sec)")
            print_newline()

        return wrapper

    return arg_wrapper
