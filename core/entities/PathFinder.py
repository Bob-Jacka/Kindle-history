import os
from pathlib import Path
from typing import TextIO

from core.entities.Formatter import Format
from data.Constants import (
    global_logger,
    CLOSE_MENU_CODE
)

# Variables:
__file_with_read_books: TextIO
"""
File where stored all books that were read
"""

# App paths:
__central_dir: str
"""
directory address where app stored (home directory path)
"""

__current_dir: str
"""
pointer to current working directory of the application
"""

__path_to_books_dir: str
"""
path where your books stored
"""

__fullpath_to_readfile: str
"""
Alias variable name for central dir + file name with read books
"""


##################Functions for data retrieving

def count_books(self):
    """
    Function for count books in read file if exists
    :return: book count in terminal
    """
    if os.path.exists(self.path_to_read_file):
        book_counter = 0
        for line in self.file_with_read_book:
            if line != '\n':
                book_counter += 1
        print(f'Books count is - {Format.underline_start + str(book_counter) + Format.underline_end}')

    else:
        print('Read book file not found!')


def get_central_dir_name():
    if __central_dir is not None:
        return __central_dir
    else:
        raise Exception('File with read books is not initialized')


def get_current_dir_name():
    if __current_dir is not None:
        return __current_dir
    else:
        raise Exception('File with read books is not initialized')





def set_current_dir(new_value: str | Path):
    """
    None safety setter function for current directory
    :param new_value: new value of current directory
    :return: None
    """
    global __current_dir
    if new_value is not None:
        __current_dir = new_value
    else:
        raise Exception('New value of current directory cannot be None')


def set_fullpath_to_readfile(new_value: str | Path):
    global __fullpath_to_readfile
    if new_value is not None:
        __fullpath_to_readfile = new_value
    else:
        raise Exception('New value of fullpath cannot be None')


def move_upper():
    """
    Move upper in file system tree
    :return: None
    """
    global __current_dir
    __current_dir = Path(__current_dir).parent


def move_lower():
    """
    Move lower in file system tree
    :return: None
    """
    global __current_dir
    p = Path('../..')  # check current directory
    dir_list = [x for x in p.iterdir() if x.is_dir()]
    Format.prGreen('Available directories:')
    if len(dir_list) == 0:
        Format.prRed('There are no directories nearby')
    else:
        dir_counter = 0  # change value to zero if you are a programmer.
        for dir in dir_list:
            print(f'{dir_counter}: {dir.name}')
            dir_counter += 1

        print()  # just empty line
        print(f'Or {CLOSE_MENU_CODE}: to exit this menu')

        while True:
            print('Enter dir number to move in')
            dir_number = int(input(CLOSE_MENU_CODE))
            if dir_number in range(len(dir_list)):
                __current_dir = dir_list[dir_number].as_posix()
                break
            elif dir_number == int(CLOSE_MENU_CODE):
                global_logger.log('Close menu')
                break
