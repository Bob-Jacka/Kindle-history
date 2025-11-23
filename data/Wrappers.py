import datetime
from typing import (
    Any,
    Callable
)


def log(function) -> Callable:
    """
    Record database function invocation with time and date.
    Can write invocation to file.
    :param function: function object to invoke
    :return: Decorator function
    """

    def wrapper(*args, **kwargs) -> Any:
        log_msg: str = f'[{datetime.datetime.now()}]: invoked function with name: "{function.__name__}"'
        colored_formated_msg = '\033[97m' + log_msg + '\033[00m'
        print(colored_formated_msg)
        r = function(*args, **kwargs)
        return r

    return wrapper


def cancelable_operation(function):
    """
    Cancel operation due to errors and restore previous condition.
    :param function: wrapped function to cancel if error occurred.
    :return: None
    """

    def cancel(*args, **kwargs):
        save_list: list = list()  # list object for saving context
        try:
            r = function(*args, **kwargs)
            return r
        except Exception as e:
            print(f'Operation: "{function.__name__}" canceled, previous condition restored')
            print(f'Exception during executing "{function.__name__}" - {e}')

    return cancel
