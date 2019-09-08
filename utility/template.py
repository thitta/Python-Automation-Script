import functools
import inspect
import time
from collections import namedtuple

from utility.print_utility import *

_context = {}

NextStep = namedtuple("TaskReturn", ("runnable", "context"))


def decorator(func):
    return func


@decorator
def procedure(message: str = None, *, user_input: bool = False, show_time: bool = False):
    """
    Decorator for a procedure in automation script

    the decorated function is expected to...
    - provide "user_input" param to accept user's input if the `use_input` is True
    - provide arbitrary key-words params
    - return a NextStep object

    :param message: prompt message
    :param user_input: if true, the message will be printed by input()
    :param show_time: if true, print execution time to the console
    """

    def decorator_wrapper(func):

        @functools.wraps(func)
        def func_wrapper():
            # print message or ask for input
            if user_input is True and message is not None:
                _context["user_input"] = input(message)
            else:
                if message is not None:
                    print(message)
            # execute
            try:
                start_time = time.time()
                next_step: NextStep = inject_context_and_run(func, _context)
                end_time = time.time()
            except Exception as e:
                raise (e)
            else:
                if show_time is True:
                    print(f" ok({round(end_time - start_time, 2)} sec)")
                # update context
                _context.update(next_step.context)
                print_newline()
                # run next step if exists
                if next_step.runnable is not None:
                    next_step.runnable()
                # or execute teardown
                else:
                    for runnable in _teardown:
                        try:
                            inject_context_and_run(runnable, _context)
                        except Exception:
                            pass

        return func_wrapper

    return decorator_wrapper


_teardown = []


@decorator
def teardown(func):
    """
    registered function into _teardown array

    all the registered functions will be executed when the script ends
    """
    _teardown.append(func)

    @functools.wraps(func)
    def wrapper():
        func()

    return wrapper


def inject_context_and_run(runnable, context):
    try:
        args = (context[key] for key in inspect.getfullargspec(runnable).args)
        return runnable(*args)
    except KeyError:
        msg = (
            f"can't inject context into function when calling {runnable.__name__}()\n"
            f"  function args: {inspect.getfullargspec(runnable).args}\n"
            f"  context keys: {list((key for key in _context.keys()))}\n"
        )
        raise DecoratorError(msg)


class DecoratorError(Exception):
    pass
