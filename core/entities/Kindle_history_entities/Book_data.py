import os
import re
from copy import copy
from pathlib import Path
from typing import (
    Literal,
    Final
)

from core.entities.Formatter import Format

type Book_type = Literal['audio', 'text']
"""
Special type for type of the book in this utility.
"""

_SAVE_POINT_EXTENSION: Final[str] = '.sdr'
"""
Extension of the file with bookmarks in cracked Kindle device. 
"""


class Book_data:
    """
    Class for encapsulating book data.
    Include dir where book stored and its name.
    """

    def __init__(self, current_storing_dir: str | os.PathLike = '.', book_name: str = '', book_category: str = '',
                 book_type: Book_type = 'text', book_author: str = ''):
        """
        Book data constructor
        :param current_storing_dir: directory where book is stored
        :param book_name: name of the book (string value)
        :param book_category: category of the book
        :param book_type: literal type
        """
        self.current_dir = current_storing_dir
        self.book_name = book_name
        self.book_type = book_type
        self.book_category = book_category
        self.book_author = book_author

    def get_current_dir(self) -> str:
        return self.current_dir

    def get_book_type(self):
        return self.book_type

    def get_book_category(self):
        return self.book_category

    def get_book_name(self) -> str:
        return self.book_name

    def get_book_author(self) -> str:
        return self.book_author

    def get_book_extension(self, book_extensions: list) -> str | None:
        """
        Receives book extension by cutting book name
        :return: string value for book extension or None if book not found
        """
        copy_book_name = copy(self.book_name)
        book_ext = copy_book_name[-1:copy_book_name.find('.')]
        if book_ext in book_extensions:
            return book_ext
        else:
            Format.prRed('Book extension does not support')

    def get_full_path(self) -> str:
        """
        Method for returning full path by concatenating current dir and book name.
        :return: string value
        """
        return self.current_dir + self.book_name

    def get_save_point_path(self) -> str:
        """
        Method for returning path to save points.
        Do not exception safe, need to check path before use.
        :return: string value
        """
        return self.current_dir + self.book_name[:self.book_name.find('.')] + _SAVE_POINT_EXTENSION

    def get_save_point_name(self) -> str:
        """
        Method for retrieving name with save point dir extension.
        Do not exception safe, need to check path before use.
        :return: name of bookmark dir
        """
        return self.book_name[:self.book_name.find('.')] + _SAVE_POINT_EXTENSION

    def has_bookmark_dir(self) -> bool:
        """
        Method for checking if bookmark dir exists
        :return: bool value of existence.
        """
        return Path(self.book_name[:self.book_name.find('.')] + _SAVE_POINT_EXTENSION).exists()

    def get_lua_data(self) -> tuple[bool, None, None] | tuple[bool, float, str] | None:
        """
        Method for receiving for book completeness.
        Decide if book is read by two parameters - 1) finished persent of book and 2) book status
        :return: tuple with parameters to decide.
        """
        book_finish_reason: list = list()
        try:
            sdr_list = os.listdir(Path(self.get_save_point_path()))
            lua_file: str
            for elem in sdr_list:
                if elem.__contains__('metadata'):
                    lua_file = elem
                else:
                    raise Exception('Sdr directory is corrupted')
            with open(lua_file) as lua_script:
                all_file: list[str] = lua_script.readlines()
                # get percent of finished book
                percent_match = re.search(r'percent_finished\s*=\s*([\d.]+)', all_file)
                percent_finished: float = float(percent_match.group(1)) if percent_match else None

                # get status parameter
                status_match = re.search(r'status\s*=\s*["\']([^"\']+)["\']', all_file)
                status: str = status_match.group(1) if status_match else None

            if len(book_finish_reason) == 3 and (percent_finished is not None and status is not None):
                return True, percent_finished, status
            else:
                return False, percent_finished, status
        except Exception as e:
            print(f'Exception while getting path to lua script - {e}')

    @staticmethod
    def decide_if_book_finished(lua_data: tuple[bool, float, str]) -> bool:
        """
        Decide if book is truly finished.

        :param lua_data: tuple with parameters to decide.
        :return: bool value of book finish.
        """
        return lua_data[0] is True and (lua_data[1] >= 0.90 or lua_data[2] == 'complete')

    def get_book_stat(self, print_or_get: bool) -> None | list[str]:
        """
        Get book data from lua script in sdr directory.
        If value of print_or_get equal to True - print into console, False - get as a list of string
        :param print_or_get: is need for print in console or get as a list.
        :return: None (if value printed) or list with lua script lines
        """
        try:
            sdr_list = os.listdir(Path(self.get_save_point_path()))
            lua_file: str
            for elem in sdr_list:
                if elem.__contains__('metadata'):
                    lua_file = elem
                else:
                    raise Exception('Sdr directory is corrupted')
            with open(lua_file) as lua_script:
                all_file: list[str] = lua_script.readlines()[2:]  # delete first line of script
                if print_or_get:
                    print('Print lua script lines')
                    for line in all_file:
                        print(line)
                else:
                    print('Return lua script lines')
                    return all_file
        except Exception as e:
            print(f'Exception while getting path to lua script - {e}')
