import io
import os
import sys
import time
from os.path import exists

from termcolor import colored

user_input_cursor: str = '>> '


def select_terminal(items_directory_path: str, is_full_path_ret: bool = False) -> str | os.PathLike | None:
    """
    Selects item to be proceeded in neuro network.
    Supports "exit" directive.
    :param is_full_path_ret: indicates if you need full path to directory or not.
    :param items_directory_path: directory where you need terminal.
    :return: path to use.
    """
    try:
        no_column_print = lambda img_counter, img_name: print(f'\t №{img_counter}. {img_name}')

        dir_container = os.listdir(items_directory_path)
        if exists(items_directory_path) and len(dir_container) != 0:
            image_counter = 0
            items_list: list[str] = list()
            for image in dir_container:
                no_column_print(img_counter=image_counter, img_name=image)
                items_list.append(image)
                image_counter += 1
            while True:
                print('Enter "exit" to break loop.')
                print('Select Item -> enter number of item.')
                print(user_input_cursor, end='')
                user_input = input()
                if user_input == 'exit' and not user_input.isdigit():
                    break
                else:
                    user_input = int(user_input)
                if user_input.is_integer() and user_input in range(len(items_list)):
                    if is_full_path_ret:
                        return f'{items_directory_path}{items_list[user_input]}'
                    else:
                        return items_list[user_input]
                else:
                    print_error('Wrong argument, try again.')
                    continue
    except Exception as e:
        print_error(f'Error occurred in Terminal function - {e.with_traceback(None)}.')


def int_input_from_user(values_range=None, topic: str = '') -> int | None:
    """
    Error safety static function for input integer number from user.
    :param values_range: accepts if inputted value in this range.
    :param topic: *optional argument.
    :return: integer number from user.
    """
    try:
        if topic != '':
            print(topic)
        print(user_input_cursor, end='')
        user_input = int(input())
        if values_range is not None:
            if user_input in range(values_range):
                print('Value in given range')
                return user_input
        return user_input
    except Exception as e:
        print_error(f'Error occurred in int_input_from_user function - {e.with_traceback(None)}.')


def str_input_from_user(topic: str = '') -> str | None:
    """
    Error safety static function for input string from user.
    :param topic: *optional argument.
    :return: string from user input or "None" if error occurred.
    """
    try:
        if topic != '':
            print(topic)
        print(user_input_cursor, end='')
        user_input = str(input())
        if not user_input.isnumeric() and not user_input.isspace():
            return user_input
    except Exception as e:
        print_error(f'Error occurred in str_input_from_user function - {e.with_traceback(None)}.')


def user_input_with_exit(values_range: int = None) -> int | str | None:
    """
    Error safety static function for input string or integer number from user, that supports exit from loop.
    Input value can be string or integer.
    :param values_range: accepts if inputted value in this range.
    :return: integer number from user or "exit" value if user wants to exit loop.
    """
    try:
        print(user_input_cursor, end='')
        user_input: int | str = input()
        if user_input.isdigit():
            user_input = int(user_input)
            if values_range is not None and user_input in values_range:
                print('Value in given range.')
                return user_input
            return user_input
        else:
            if user_input == 'exit':
                return user_input
    except Exception as e:
        print_error(f'Error occurred in input_from_user function - {e.with_traceback(None)}.')


def print_error(msg: str):
    """
    Static function for printing error with red color.
    :param msg: message to print.
    """
    print(colored(msg, 'red'))


def print_success(msg: str):
    """
    Static function for printing success with green color.
    :param msg: message to print.
    """
    print(colored(msg, 'green'))


def print_info(msg: str):
    """
    Static function for printing info messages with blue color.
    :param msg: message to print.
    """
    print(colored(msg, 'blue'))


def is_binary(stream):
    mode = getattr(stream, 'mode', None)
    if mode:
        return 'b' in mode
    return not isinstance(stream, io.TextIOBase)


# def prints(*a, **kw):
#     """
#     Print either unicode or bytes to either binary or text mode streams
#     """
#     stream = kw.get('file', sys.stdout)
#     if stream is None:
#         return
#     sep, end = kw.get('sep'), kw.get('end')
#     if sep is None:
#         sep = ' '
#     if end is None:
#         end = '\n'
#     if is_binary(stream):
#         encoding = getattr(stream, 'encoding', None) or 'utf-8'
#         a = (as_bytes(x, encoding=encoding) for x in a)
#         sep = as_bytes(sep)
#         end = as_bytes(end)
#     else:
#         a = (as_unicode(x, errors='replace') for x in a)
#         sep = as_unicode(sep)
#         end = as_unicode(end)
#     for i, x in enumerate(a):
#         if sep and i != 0:
#             stream.write(sep)
#         stream.write(x)
#     if end:
#         stream.write(end)
#     if kw.get('flush'):
#         try:
#             stream.flush()
#         except Exception:
#             pass


# def debug_print(*args, **kw):
#     '''
#     Prints debug information to the console if debugging is enabled.
#
#     This function prints a message prefixed with a timestamp showing the elapsed time
#     since the first call to this function. The message is printed only if debugging is enabled.
#
#     Parameters:
#     *args : tuple
#         Variable length argument list to be printed.
#     **kw : dict
#         Arbitrary keyword arguments to be passed to the `print` function.
#
#     Attributes:
#     base_time : float
#         The timestamp of the first call to this function. Stored as an attribute of the function.
#
#     Behavior:
#     - On the first call, initializes `base_time` to the current time using `time.monotonic()`.
#     - If `is_debugging()` returns True, prints the elapsed time since `base_time` along with the provided arguments.
#     '''
#     from calibre.constants import is_debugging
#
#     # Get the base_time attribute, initializing it on the first call
#     base_time = getattr(debug_print, 'base_time', None)
#     if base_time is None:
#         # Set base_time to the current monotonic time if it hasn't been set
#         debug_print.base_time = base_time = time.monotonic()
#
#     # Check if debugging is enabled
#     if is_debugging():
#         # Print the elapsed time and the provided arguments if debugging is enabled
#         prints(f'DEBUG: {time.monotonic() - base_time:6.1f}', *args, **kw)
