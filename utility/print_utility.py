from typing import Iterable, Any


def print_init_message(script_name: str):
    print_fence(f"{script_name} script")
    print_newline()


def print_end_message(script_name: str):
    print_fence(f"{script_name} completed!")
    print_newline()


def print_iterable_by_line(iterable: Iterable[Any]):
    for v in iterable:
        print(v)


def print_fence(msg: str = None, fillchar: str = "-", length: int = 60):
    if msg is None:
        print(fillchar * length)
    else:
        print(fillchar * length)
        print(msg)
        print(fillchar * length)


def print_header(msg: str, fillchar: str = "-", length: int = 60):
    if length - len(msg) <= 4:
        print(msg)
    else:
        msg = " " + msg + " "
        msg = msg.rjust(int((length - len(msg)) / 2) + len(msg), fillchar)
        msg = msg.ljust(length, fillchar)
        print(msg)


def print_newline(count: int = 1):
    for _ in range(count):
        print()
