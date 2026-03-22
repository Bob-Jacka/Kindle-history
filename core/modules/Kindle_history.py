"""
Kindle history module
Store your read books in file or delete already read book from your e-book, like Kindle

Module gives you an interactive way of using your e-book

*Module only responsible for read file actions
"""
import os

from data.Wrappers import log

try:
    from core.entities.Book_data import Book_data
    from data.Constants import (
        INPUT_SYM,
        CLOSE_MENU_CODE, STATIC_DIR_NAME_FOR_FAV
    )

    from core.entities.Formatter import Format
    from enum import Enum

    from core.entities.AbstractModule import Module

    import datetime
    import inspect
    import sys
    import abc
    from copy import copy
    from pathlib import Path
    from typing import (
        override,
        TextIO,
        Final,
        Literal
    )
except Exception as e:
    print(f'An exception occurred during dependencies import - {e}')


class Kindle_history(Module):

    def __init__(self, cli_parameters: list[str]):
        self.config = None
        self.local_logger = None
        self.readFile = None
        self.parameters = cli_parameters

    @log
    def post_init(self, app_config):
        self.config = app_config
        self.local_logger = app_config.get_logger()
        self.readFile = app_config.get_read_file_name()

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
        if len(split_line) < 3 and len(split_line) == 1:  # case of no such format
            to_return['name'] = str(split_line)
            self.local_logger.log('Wrong format string in parsing found')
            return to_return
        to_return['name'] = split_line[0]
        to_return['author'] = split_line[1]
        to_return['date'] = split_line[2]
        return to_return

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
        stored_fav_books = os.listdir(self.config.path_to_dir_with_app() + STATIC_DIR_NAME_FOR_FAV)
        if len(stored_fav_books) == 0:
            return []
        else:
            stored_fav_books.remove('.')
            for stored_book in stored_fav_books:
                pass
            if len(fav_books) != 0:
                return fav_books
            else:
                return []

    @log
    def add_new_book_to_history(self, book_data: Book_data):
        """
        :param book_data: tuple with book info, where first argument is path to book and second argument is book name
        :return: None
        """
        if book_data is not None:
            try:
                book_name: str  # name of the book to proceed
                pass
            except Exception as e:
                self.local_logger.log(f'Exception while adding new book - {e}')

    @log
    def count_books(self):
        """
        Function for count books in read file if exists
        :return: book count in terminal
        """
        if self.book_county != 0:
            book_counter = 0
            for line in self.readfile:
                if line != '\n':
                    book_counter += 1
                self.book_county = book_counter
                print(f'Books count is - {Format.underline_start + str(book_counter) + Format.underline_end}')
        else:
            print(f'Books count is - {Format.underline_start + str(self.book_county) + Format.underline_end}')

    @log
    def find_book(self, book_to_find) -> None:
        """
        Function for finding book in read file, by providing book name or name part.
        :return: None
        """
        while True:
            if book_to_find != '' and book_to_find is not None:
                for book in self.readfile:
                    if book.find(book_to_find):
                        Format.prGreen('Book found')
                        break
                    else:
                        Format.prRed('Book not found')
                        break
                break  # exit loop if book found or not

    @log
    def check_for_duplicates(self) -> None:
        """
        Check for duplicates in read file and output useful message about
        :return: None
        """
        all_data = self.readfile.readlines()
        is_found: bool = False
        for book_name in all_data:
            count = all_data.count(book_name)
            if count >= 2:
                is_found = True
                print(f'Duplicate found with name {book_name} for {count} times')
        if not is_found:
            print('No duplicates found')

    @log
    def is_need_for_new_line(self) -> bool:
        """
        Super dummy function for checking if you need new line symbol in read file.
        :return: bool value if you need for new line in read file
        """
        books_counter: int = 0
        new_line_counter: int = 0
        while True:
            line = self.readfile.readline()

            if line.endswith('\n'):
                new_line_counter += 1

            if line == '':
                break

            books_counter += 1
        if books_counter > new_line_counter:
            return True
        elif books_counter == new_line_counter:
            return False
        else:
            return False
