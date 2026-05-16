import os
from copy import copy
from pathlib import Path
from typing import (
    Literal,
    Final
)

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
    Class for encapsulating book data for Kindle_history module.
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
        self.__current_dir = current_storing_dir
        self.__book_name = book_name
        self.__book_type = book_type
        self.__book_category = book_category
        self.__release_data = None
        self.__when_read = None
        self.__book_author = book_author

    def get_current_dir(self) -> str:
        return self.__current_dir

    def get_book_type(self) -> str:
        return self.__book_type

    def get_book_category(self) -> str:
        return self.__book_category

    def get_book_name(self) -> str:
        return self.__book_name

    def get_book_author(self) -> str:
        return self.__book_author

    def get_release_data(self) -> str:
        return self.__release_data

    def get_when_read(self) -> str:
        return self.__when_read

    def set_book_type(self, new_type) -> None:
        self.__book_type = new_type

    def set_book_category(self, new_category) -> None:
        self.__book_category = new_category

    def set_book_name(self, new_book_name) -> None:
        self.__book_name = new_book_name

    def set_book_author(self, new_author_name) -> None:
        self.__book_author = new_author_name

    def set_release_data(self, release_data) -> None:
        self.__release_data = release_data

    def set_when_read(self, when_read) -> None:
        self.__when_read = when_read

    def get_full_path(self) -> str:
        """
        Method for returning full path by concatenating current dir and book name.
        :return: string value
        """
        return self.__current_dir + self.__book_name

    def get_save_point_path(self) -> str:
        """
        Method for returning path to save points.
        Do not exception safe, need to check path before use.
        :return: string value
        """
        return self.__current_dir + self.__book_name[:self.__book_name.find('.')] + _SAVE_POINT_EXTENSION

    def get_save_point_name(self) -> str:
        """
        Method for retrieving name with save point dir extension.
        Do not exception safe, need to check path before use.
        :return: name of bookmark dir
        """
        return self.__book_name[:self.__book_name.find('.')] + _SAVE_POINT_EXTENSION

    def has_bookmark_dir(self) -> bool:
        """
        Method for checking if bookmark dir exists
        :return: bool value of existence.
        """
        return Path(self.__book_name[:self.__book_name.find('.')] + _SAVE_POINT_EXTENSION).exists()

    def get_short_name(self):
        """
        Get book name in short notation.
        :return: Book name
        """
        short_book_name: str
        if len(self.__book_name) > 80:
            short_book_name = copy(self.__book_name)[0:80] + '...'
        else:
            short_book_name = copy(self.__book_name)
        return short_book_name

    def __str__(self) -> str:
        """
        String representation of Book_data object.
        :return: formatted string with book info
        """
        return (f"Book_data(name='{self.__book_name}', "
                f"author='{self.__book_author}', "
                f"type={self.__book_type}, "
                f"category='{self.__book_category}', "
                f"dir='{self.__current_dir}')")

    def __repr__(self) -> str:
        return (f"Book_data(current_storing_dir='{self.__current_dir}', "
                f"book_name='{self.__book_name}', "
                f"book_category='{self.__book_category}', "
                f"book_type={self.__book_type!r}, "
                f"book_author='{self.__book_author}')")
