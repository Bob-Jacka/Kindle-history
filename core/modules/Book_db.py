"""
Module for small, inner Nosql database for books and book actions.
Contains CRUD action list for using and some special syntax to use interactive
"""

import datetime
import enum
import os
from os import PathLike
from typing import (
    Final,
    Literal
)

from core.entities.AbstractModule import Module
from core.other.Utils import str_input_from_user

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


class __Book_db_translation(enum.Enum):
    """
    Translation unit for book db.
    Localizes database syntax
    """
    pass


class Book_db(Module):
    """
    Custom database for storing information about books on your e-book
    """

    class Syntax_interpreter:
        """
        Class responsible for syntax interpretation in interactive (or not) mode.
        Interpreter for BQL (book query language).
        Map contains key for fast retrieving element and tuple with two fields, where first field is syntax word
        and second field is help description for words and its usage.
        """
        syntax_rules: Final[dict[str, tuple[str, str]]] = {
            # main operators in database
            'choose': tuple(('choose', 'like select word in sql, can take parameters for selecting: all or row name')),
            'delete': tuple(('delete', 'can delete record in table or table')),
            'create': tuple(('create', 'can create table object with parameters')),
            'update': tuple(('update', 'update records in table object')),
            'add': tuple(('add', 'add record to the table, require table name')),

            # embedded functions
            'sync': tuple(('sync', 'synchronize records between your local pc and e-book')),
            'reg': tuple(('reg', 'word for regular expressions, take string object as a parameter')),

            # other words
            'help': tuple(('help', 'special operator for help users in their usage of BQL syntax')),
            'all': tuple(('all', 'special word for selecting or deleting all records in database')),
            'in': tuple(('in', 'like "from" word in sql')),

            # entity words
            'table': tuple(('table', 'word for table in database, contains parameters: name, order or limit')),
            'record': tuple(('record', 'word for record in table'))
        }
        """
        Examples of BQL syntax:
        1. choose <record> in <table_name> (select statement)
            1.1 choose Record(name="1984", <optional book type>, <optional read time>) in Table(name="customers")
            1.2 CHOOSE RECORD(name="some book") in Table(name="books") (Operators can be in upper or lower case)
            
        2. delete <record> in <table_name> (delete statement)
            delete Record(name="Harry potter", <optional book type>, <optional read time>) in Table(name="customers")
            
        3. synk (synchronize data between database and e-book)
        
        4. create Table(name=<required parameters name>) - (creates table with given parameters)
        
        5. add Record(name='We') in Table(name="tableName")
        
        6. update Record(name='Brave new world') in Table(name='Anti_utopias') 
            6.1 update Record(name=reg('45 ')) in Table(name=reg('Anti'))
            - you can use 'reg' word for regular expressions if you do not remember full name
        
        Other examples: Choose all in Table(name="math", order=desk, limit=10) - descending select from all from 
        table named math and limit by 10 records"""

        class _Database_core:
            """
            Order of execution:
            1. first you need to create database object
            2. second create tables in your database
            3. and last create records in tables
            """

            class Database:
                """
                Upper level entity in book_db
                """

                class Table:

                    """
                    Quant of book database storage.
                    """

                    class Record:
                        """
                        Quant of book database storage table.
                        Record consists of next columns:
                        0. id - unique identifier of the book
                        1. Book name - name of the book (1-80) - Required parameter
                        2. Book category (type ex. Math)
                        3. Read date (datetime or '-' if not read yet)
                        4. Book type - can be text or audio (for audiobooks)
                        """

                        type Book_type = Literal['text', 'audio']

                        def __init__(self, id: int, book_name: str, book_category: str = '', read_time: str = '',
                                     book_type: Book_type = 'text'):
                            self.id = id
                            self.book_name = book_name
                            self.book_category = book_category
                            self.read_time = read_time
                            self.type = book_type

                        def get_book_id(self):
                            return self.id

                        def get_book_name(self):
                            return self.book_name

                        def get_dir_name(self):
                            return self.book_category

                        def get_read_time(self):
                            return self.read_time

                        def get_book_type(self):
                            return self.type

                        def to_string(self) -> str:
                            return f'{self.book_name}{RECORD_SEP}{self.book_category}{RECORD_SEP}{self.read_time}'

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

                table: list[Table] = None

                def __init__(self):
                    self.tables = list()

                @cancelable_operation
                def create_table(self, table_name: str) -> None:
                    """
                    Creates new file, called table in terms of book database.
                    :return: None
                    """
                    try:
                        new_table = self.Table(table_name)
                        self.tables.append(new_table)
                    except Exception as e:
                        print(f'An exception occurred during creating table - {e}')

                @cancelable_operation
                def delete_table(self, table_name: str) -> None:
                    pass

                def get_tables(self):
                    return self.tables

            def __int__(self):
                pass

            @cancelable_operation
            def create_database(self):
                try:
                    self.database = self.Database()
                except Exception as e:
                    print()

            @cancelable_operation
            def synchronize(self) -> None:
                """
                Method for synchronizing e-book files and database tables
                :return: None
                """
                pass

        def __int__(self):
            self.database_core = self._Database_core()

        @log_record_action
        def parse_sentence(self, sentence: str) -> None:
            """
            Parse given sentence in BQL and invoke functions.
            :param sentence: sentence in book query language.
            :return: None
            """
            lexemes = sentence.split(' ')
            if lexemes[0].lower() in self.syntax_rules.keys():
                operator = lexemes[0]
                match operator:
                    case 'help':
                        self.print_help()
                    case 'select':
                        self.__parse_select_operator(lexemes=lexemes)
                    case 'delete':
                        self.__parse_delete_operator(lexemes=lexemes)
                    case 'create':
                        self.__parse_create_operator(lexemes=lexemes)
                    case 'add':
                        self.__parse_add_operator(lexemes=lexemes)
                    case 'sync':
                        self.__parse_sync_operator()
                    case _:
                        raise RuntimeError(
                            f'Unknown operator given - {operator}'
                        )  # yeah, I know that I handle this problem
            else:
                raise RuntimeError('Sentence should start with one of the operators')

        @log_record_action
        def __parse_select_operator(self, lexemes: list[str]):
            pass

        @log_record_action
        def __parse_delete_operator(self, lexemes: list[str]):
            pass

        @log_record_action
        def __parse_create_operator(self, lexemes: list[str]):
            pass

        @log_record_action
        def __parse_update_operator(self, lexemes: list[str]):
            pass

        @log_record_action
        def __parse_add_operator(self, lexemes: list[str]):
            pass

        @log_record_action
        def __parse_sync_operator(self):
            self.database_core.synchronize()

        @log_record_action
        def print_help(self):
            print('This module is responsible for database functionality')
            print('Here are words that used')
            for _, value in self.syntax_rules:
                print(f'{value[0]} word contains next comment: {value[1]}')

    def __init__(self, is_interactive_mode: bool = None, start_point: str | PathLike = '.'):
        self.is_interactive = is_interactive_mode
        self.syntax_interpreter = self.Syntax_interpreter()
        self.start_point = start_point
        self.tables: list[Book_db.Syntax_interpreter._Database_core.Table]  # table of database, string values of names
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

    @log_record_action
    def __run_interactive(self):
        while True:
            print('Enter command to run in interpreter or "close" to close: ', end='')
            user_command_line = input()
            if user_command_line != '':
                if user_command_line != 'close':
                    self.syntax_interpreter.parse_sentence(user_command_line)
                else:
                    break
            else:
                print('Entered empty command, try again')
                continue

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
            if self.is_interactive is None:
                while True:
                    print('Run module interactively or not?')
                    choice = str_input_from_user()
                    if choice == 'yes':
                        self.__run_interactive()
                        break
                    else:
                        self.__run_non_interactive()
                        break
            else:
                if self.is_interactive:
                    self.__run_interactive()
                else:
                    self.__run_non_interactive()
        except Exception as e:
            print(f'An exception in run module method - {e}')
