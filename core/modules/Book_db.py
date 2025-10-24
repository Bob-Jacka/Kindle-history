"""
Module for small, inner database for books and book actions.
Contains CRUD action list for using and some special syntax to use interactive
"""

import datetime
import os
from os import PathLike
from typing import Final

from core.entities.AbstractModule import Module

RECORD_SEP: Final[str] = '|'
USER_INPUT_SYM: Final[str] = '>> '
LOG_FILE_NAME: Final[str] = f'db_logs_{datetime.datetime.now()}.logs'


def log_record_action(function, is_file_write: bool = False):
    """
    Record database function invocation with time and date.
    Can write invocation to file.
    :param is_file_write: is need for file output
    :param function: input function to wrap
    :return: None
    """

    def logger():
        log_msg: str = f'[{datetime.datetime.now()}]: invoked database function with name: "{function.__name__}"'
        print(log_msg)
        function()
        if is_file_write:
            with open(LOG_FILE_NAME) as log_file:
                log_file.write(log_msg)

    return logger


@log_record_action(True)
def cancelable_operation(function):
    """
    Cancel operation due to errors and restore previous condition.
    :param function: wrapped function to cancel if error occurred.
    :return: None
    """

    def cancel(*args, **kwargs):
        print(f'Operation: "{function.__name__}" canceled, previous condition restored')
        try:
            function(*args, **kwargs)
        except Exception as e:
            print(f'Exception during executing "{function.__name__}" - {e}')

    return cancel


class Book_db_translation:
    """
    Translation unit for book db.
    Localizes database syntax
    """
    pass


class Book_db(Module):
    """
    Custom database for storing information about books on your e-book
    """

    class Record:
        """
        Quant of book database storage table.
        Record consists of next columns:
        1. Book name - name of the book (1-80)
        2. Book directory (type ex. Math)
        3. Read date (datetime or '-' if not read yet)
        """

        def __init__(self, book_name: str, dir_name: str = '', read_time: str = ''):
            self.book_name = book_name
            self.dir_name = dir_name
            self.read_time = read_time

        def get_book_name(self):
            return self.book_name

        def get_dir_name(self):
            return self.dir_name

        def get_read_time(self):
            return self.read_time

        def to_string(self) -> str:
            return f'{self.book_name}{RECORD_SEP}{self.dir_name}{RECORD_SEP}{self.read_time}'

    class Table:
        """
        Quant of book database storage.
        """

        def __init__(self, table_name: str):
            self.table_name = table_name
            # initialize table and create file
            self.__init_table()

        def get_table_name(self):
            return self.table_name

        @cancelable_operation
        def add_record(self, record):
            pass

        @cancelable_operation
        def update_record(self, table_name: str, identifier: str):
            pass

        @cancelable_operation
        def delete_record(self, table_name: str, identifier: str):
            pass

        @log_record_action
        def select_records(self) -> None:
            """
            Select from already read and e-book files
            :return: None
            """
            pass

        def __init_table(self):
            if not os.path.exists(self.table_name):
                with open(self.table_name, 'w+'):
                    pass
            else:
                print('Table already exists')

    class Syntax_interpreter:
        """
        Class responsible for syntax interpretation in interactive (or not) mode.
        Interpreter for BQL (book query language)
        """
        syntax_rules: Final[dict[str, str]] = {
            'select_word': 'choose',  # like 'select' word
            'delete_word': 'delete',
            'create_word': 'create',
            'update_word': 'update',

            'in_word': 'in',  # like 'from' word in sql
            'with_word': '',
            'table_word': 'table',  # if you want to create table in interactive mode
            'record_word': 'record'  # if you want to create record in interactive mode
        }
        """
        Examples of BQL syntax:
        1. choose <record> in <table_name> (select statement)
            choose Record("1984", <optional book type>, <optional read time>) in customers
        2. delete <record> in <table_name> (delete statement)
            delete Record("Harry potter", <optional book type>, <optional read time>) in customers
        """

        def parse_sentence(self, sentence: str) -> None:
            lexemes = sentence.split(' ')
            if lexemes[0] in self.syntax_rules:
                pass
            else:
                raise RuntimeError('Sentence should start with one of the operators')

    def __init__(self, is_interactive_mode: bool, start_point: str | PathLike = '.'):
        self.is_interactive = is_interactive_mode
        self.syntax_interpreter = self.Syntax_interpreter()
        self.start_point = start_point
        self.tables: list[Book_db.Table]  # table of database, string values of names
        # init inner database structure
        self.__init_database()

    def __init_database(self) -> None:
        """
        Initialize database by checking for table files
        :return: None
        """
        tables = os.listdir(self.start_point)

    def __change_table(self):
        pass

    @staticmethod
    def __get_table_view(file_descriptor) -> list[str]:
        """
        Read all lines from database and return list with lines
        :param file_descriptor: file descriptor to use
        :return: list with lines (records)
        """
        return file_descriptor.readlines()

    @staticmethod
    def __generate_table_name(init_table_name: str) -> str:
        return f'table-{init_table_name}'

    @cancelable_operation
    def create_table(self, table_name: str) -> None:
        """
        Creates new file, called table in terms of book database.
        :return: None
        """
        try:
            new_table = self.Table(table_name)

        except Exception as e:
            print()

    @cancelable_operation
    def delete_table(self, table_name: str) -> None:
        pass

    @cancelable_operation
    def synchronize(self) -> None:
        """
        Method for synchronizing e-book files and database tables
        :return: None
        """
        pass

    @log_record_action
    def __run_interactive(self):
        while True:
            print('Enter command to run in interpreter:')
            user_command_line = input(USER_INPUT_SYM)
            self.syntax_interpreter.parse_sentence(user_command_line)

    @log_record_action
    def __run_non_interactive(self):
        while True:
            print('Enter command number to run:')
            print('1. Select all from all tables')
            print('2. Synchronize tables in local and e-book')
            print('3. Close interactive mode')
            try:
                user_command_number: int = int(input(USER_INPUT_SYM))
                match user_command_number:
                    case 1:
                        pass
                    case 2:
                        pass
                    case 3:
                        break
                    case _:
                        print('Wrong command number, try again')
                        continue
            except Exception as e:
                pass

    @log_record_action
    def run_module(self) -> None:
        """
        Main entry point to database actions.
        Can be interactive (in cli by bql (book query language)) or just pick commands from list
        :return: None
        """
        try:
            if self.is_interactive:
                self.__run_interactive()
            else:
                self.__run_non_interactive()
        except Exception as e:
            print(f'An exception in run module method - {e}')
