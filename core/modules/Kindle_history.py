"""
Kindle history module

Responsible for local storage of history (on e-book device) and on remote targets
"""
import datetime
import os
from enum import Enum
from typing import (
    Literal,
    Any
)

import yadisk

from core.entities.AbstractModule import Module
from core.entities.Book_data import Book_data
from data.Constants import (
    STATIC_DIR_NAME_FOR_FAV
)
from data.Tokens import TOKEN_YANDEX
from data.Wrappers import log


class Memorize:
    """
    This module is responsible for storing history in different data storages.
    For example in Yandex Drive or Google Drive and maybe in local storage;

    Decentralized storage

    You can say that this functionality might be in Kindle history module, but I say No
    """

    def __init__(self, app_config, logger):
        self.config = app_config
        self.local_logger = logger

    # Data getters
    @log
    def __get_with_yandex(self, book):
        client = yadisk.Client(token=TOKEN_YANDEX)
        with client:
            pass

    @log
    def __get_with_google(self, book):
        pass

    @log
    def __get_local(self, book):
        pass

    # Data setters
    @log
    def __add_with_yandex(self, book) -> bool:
        client = yadisk.Client(token=TOKEN_YANDEX)
        with client:
            return True

    @log
    def __add_with_google(self, book) -> bool:
        pass

    @log
    def __add_local(self, book) -> bool:
        try:
            with open(self.config.path_to_read_file(), 'a+') as file_to_write:
                file_to_write.write(str(book.get_book_name()) + ' | ')
                file_to_write.write(str(book.get_book_author()) + ' | ')
                file_to_write.write(str(datetime.datetime.now().year) + ' | ')
                file_to_write.write(str(book.get_book_type()))
                file_to_write.write('\n')
                return True
        except Exception as e:
            self.local_logger.log(f'Exception while adding new book - {e}')
            return False

    # Find methods

    @log
    def __find_yandex(self, book_to_find) -> bool | None:
        pass

    @log
    def __find_google(self, book_to_find) -> bool | None:
        pass

    @log
    def __find_local(self, book_to_find) -> bool | None:
        while True:
            if book_to_find != '' and book_to_find is not None:
                with open(self.config.path_to_read_file()) as read_file:
                    for book in read_file:  # linear search
                        if book.find(book_to_find):
                            self.local_logger.log('Book found')
                            return True
                        else:
                            self.local_logger.log('Book not found')
                            return False
            self.local_logger.log('Error occurred, book maybe equals to None')
            break  # exit loop if book found or not

    # Main entry points

    @log
    def get(self, book: Book_data, mode: Literal['all', 'google', 'yandex', 'only-local']):
        getter: Any = None
        match mode:
            case 'all':
                getter = self.__get_local, self.__add_with_google, self.__add_with_yandex
            case 'google':
                getter = self.__get_with_google
            case 'yandex':
                getter = self.__get_with_yandex
            case 'only-local':
                getter = self.__get_local
            case _:
                self.local_logger.log(f'Got unknown parameter - {mode}')
                raise Exception('Unknown mode')
        getter(book)

    @log
    def add(self, book: Book_data, mode: Literal['all', 'google', 'yandex', 'only-local']) -> bool:
        storage: Any = None
        match mode:
            case 'all':
                storage = self.__add_local, self.__add_with_google, self.__add_with_yandex
            case 'google':
                storage = self.__add_with_google
            case 'yandex':
                storage = self.__add_with_yandex
            case 'only-local':
                storage = self.__add_local
            case _:
                self.local_logger.log(f'Got unknown parameter - {mode}')
                raise Exception('Unknown mode')
        return storage(book)

    @log
    def find(self, book: Book_data, mode: Literal['all', 'google', 'yandex', 'only-local']):
        finder: Any = None
        match mode:
            case 'all':
                finder = self.__find_local, self.__find_google, self.__find_yandex
            case 'google':
                finder = self.__find_google
            case 'yandex':
                finder = self.__find_yandex
            case 'only-local':
                finder = self.__find_local
            case _:
                raise Exception('Unknown mode')
        return finder(book)


class book_type(Enum):
    Text = 'Text'
    Audio = 'Audio'


class Kindle_history(Module):

    def __init__(self, cli_parameters: list[str]):
        self.config = None
        self.local_logger = None
        self.memorize_module = None
        self.readFile = None
        self.parameters = cli_parameters

    @log
    def post_init(self, app_config):
        self.config = app_config
        self.local_logger = app_config.get_logger()
        self.readFile = app_config.get_read_file_name()
        self.memorize_module = Memorize(app_config=app_config, logger=self.local_logger)

    @log
    def run_module_web(self) -> None:
        pass

    def __parse_line(self, line: str) -> dict[str, str]:
        """
        Split line into map, ex. <book name>|<book author>|<book release year>
        :param line: line of book text
        :return: dict with data
        """
        split_line = line.split('|')
        to_return: dict[str, str] = dict()
        if len(split_line) < 4 and len(split_line) == 1:  # case of no such format
            to_return['name'] = str(split_line)
            to_return['author'] = '-'
            to_return['date'] = '-'
            to_return['type'] = '-'
            self.local_logger.log('Wrong format string in parsing found')
            return to_return
        else:
            to_return['name'] = split_line[0]
            to_return['author'] = split_line[1]
            to_return['date'] = split_line[2]
            to_return['type'] = split_line[3]
            return to_return

    @log
    def get_config(self):
        return self.config

    @log
    def list_all_read_book(self) -> list[dict]:
        """
        Function for output all books that have been red.
        outputs only files with books extensions.
        :return: None
        """
        list_with_history: list[dict] = []
        with open(self.config.path_to_read_file()) as file_with_history:
            for line in file_with_history:
                list_with_history.append(self.__parse_line(line))
        return list_with_history

    @log
    def list_favourite_books(self) -> list[dict]:
        """
        Function for listing favourite books (books that saved in home directory)
        :return: None
        """
        fav_books: list[dict] = list()
        stored_fav_books = os.listdir(self.config.path_to_stored_books())
        if len(stored_fav_books) == 0:
            return []
        else:
            for stored_book in stored_fav_books:
                fav_books.append(self.__parse_line(stored_book))
            if len(fav_books) != 0:
                return fav_books
            else:
                return []

    @log
    def add_book_to_history(self, book: Book_data):
        """
        :param book: where first argument is path to book and second argument is book name
        :return: None
        """
        if book is not None:
            return self.memorize_module.add(book, 'only-local')
        else:
            self.local_logger.log('Failed to add book into history')
            return False

    @log
    def count_all_books(self) -> tuple[list[dict], list[dict], int]:
        """
        Function for count books in read file if exists
        :return: book count
        """
        all_books: list[dict] = self.list_all_read_book()
        fav_books: list[dict] = self.list_favourite_books()
        count = len(all_books) + len(fav_books)
        return tuple((all_books, fav_books, count))

    @log
    def find_book(self, book_to_find: str) -> bool | None:
        """
        Function for finding book in read file, by providing book name or name part.
        :return: None
        """
        return self.memorize_module.find(book_to_find, 'only-local')

    @log
    def check_for_duplicates(self) -> None:
        """
        Check for duplicates in read file and output useful message about
        :return: None
        """
        all_data = self.readFile.readlines()
        is_found: bool = False
        for book_name in all_data:
            count = all_data.count(book_name)
            if count >= 2:
                is_found = True
                self.local_logger.log(f'Duplicate found with name {book_name} for {count} times')
        if not is_found:
            self.local_logger.log('No duplicates found')

    @log
    def is_need_for_new_line(self) -> bool:
        """
        Super dummy function for checking if you need new line symbol in read file.
        :return: bool value if you need for new line in read file
        """
        books_counter: int = 0
        new_line_counter: int = 0
        lines = open(self.config.path_to_read_file).readlines()
        while True:
            file_lines = lines[books_counter]
            if file_lines.endswith('\n'):
                new_line_counter += 1

            if file_lines == '':
                break

            books_counter += 1
        if books_counter > new_line_counter:
            return True
        elif books_counter == new_line_counter:
            return False
        else:
            return False
