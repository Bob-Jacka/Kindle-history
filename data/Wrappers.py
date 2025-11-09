import datetime
from typing import (
    Any,
    Final,
    Callable
)

LOG_FILE_NAME: Final[str] = f'db_logs_{datetime.datetime.now()}.log'


def log(is_file_write: bool = False) -> Callable:
    """
    Record database function invocation with time and date.
    Can write invocation to file.
    :param is_file_write: is need for file output
    :return: Decorator function
    """

    def decorator(function):
        def wrapper(*args, **kwargs) -> Any:
            log_msg: str = f'[{datetime.datetime.now()}]: invoked database function with name: "{function.__name__}"'
            print(log_msg)
            r = function(*args, **kwargs)
            if is_file_write:
                try:
                    with open(LOG_FILE_NAME, 'a') as log_file:
                        log_file.write(log_msg + '\n')
                except IOError as e:
                    print(f"Ошибка записи в лог-файл: {e}")
            return r

        return wrapper

    return decorator


@log
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
