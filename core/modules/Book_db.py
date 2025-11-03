"""
Module for small, inner Nosql database for books and book actions.
Contains CRUD action list for using and some special syntax to use interactive
"""

import datetime
import enum
import os
import types
from os import PathLike
from typing import (
    Final,
    Literal,
    Generic,
    TypeVar,
    Callable,
    Any
)

from core.entities.AbstractModule import Module
from core.exceptions.DatabaseException import (
    DatabaseException,
    SyntaxInterpreterException
)
from core.other.Utils import str_input_from_user

USER_INPUT_SYM: Final[str] = '>> '
LOG_FILE_NAME: Final[str] = f'db_logs_{datetime.datetime.now()}.log'


def log(is_file_write: bool = False) -> Callable:
    """
    Record database function invocation with time and date.
    Can write invocation to file.
    :param is_file_write: is need for file output
    :return: Decorator function
    """

    def decorator(function: Callable) -> Callable:
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


class __Book_db_translation(enum.Enum):
    """
    Translation unit for book db.
    Localizes database syntax
    """
    pass


class Book_db(Module):
    """
    Custom nosql database for storing information about books on your e-book
    """

    class Syntax_interpreter:
        """
        Class responsible for syntax interpretation in interactive (or not) mode.
        Interpreter for BQL (book query language).
        Map contains key for fast retrieving element and tuple with two fields, where first field is syntax word
        and second field is help description for words and its usage.
        """
        __syntax_rules: Final[dict[str, tuple[str, str]]] = {
            # main operators in database:
            'choose': tuple(
                ('choose', 'like "select" word in sql, can take parameters for selecting: all or row name')),
            'delete': tuple(('delete', 'can delete record in table or table (cancelable operation)')),
            'create': tuple(
                ('create', 'can create table | database or record object with parameters (cancelable operation)')),
            'update': tuple(('update', 'update records in table object (cancelable operation)')),
            'add': tuple(('add', 'add record to the table, require table name (cancelable operation)')),

            # embedded functions to use:
            'sync': tuple(('sync', 'synchronize records between your local pc and e-book')),
            'reg': tuple(('reg', 'word for regular expressions, take string object as a parameter and find string')),

            # other words:
            'help': tuple(('help', 'special operator for help users in their usage of BQL syntax')),
            'all': tuple(('all', 'special word for selecting or deleting all records in database')),
            'in': tuple(('in', 'like "from" word in sql')),
            'using': tuple(('using', '')),

            # entity words:
            'database': tuple(('database', 'word for creating database')),
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
            
        3. sync (synchronize data between database and e-book, require no parameters)
        
        4. create Table(name=<required parameters name>) in Database(name=<db_name>) - (creates table with given parameters)
            4.1 create Database(name=standard_db)
        
        5. add Record(name='We') in Table(name="tableName")
        
        6. update Record(name='Brave new world') in Table(name='Anti_utopias') 
            6.1 update Record(name=reg('45 ')) in Table(name=reg('Anti'))
            - you can use 'reg' word for regular expressions if you do not remember full name
            
        7. using Database(name=db_name_to_use) - use database as main database in utility, all table actions will be 
        using with tables in this database
            7.1 Delete Database(name=db_name) - delete database 
            7.2 Create Database(name=db_name) - And you can create database, other CRUD actions are not allowed
        
        Other examples: Choose all in Table(name="math", order=desk, limit=10) - descending select from all from 
        table named math and limit by 10 records"""

        class _Database_core:
            """
            Order of execution:
            1. first you need to create database object
            2. second create tables in your database
            3. and last create records in tables
            4. And fourth, use it...
            """

            class _Database:
                """
                Upper level entity in book_db.
                Contains tables and actions with them.
                """

                T = TypeVar('T')  # Generic type of table

                class _Table(Generic[T]):
                    """
                    Quant of book database storage.
                    """

                    class _Record:
                        """
                        Quant of book database storage table.
                        Record consists of the next columns:
                        id, Book name, Book category, Read date, Book type
                        """

                        type __Book_type = Literal['text', 'audio']

                        def __init__(self, identifier: int, book_name: str, book_category: str = '',
                                     read_date: str = '',
                                     book_type: __Book_type = 'text'):
                            """
                            Wrapper class for record in database, take book data class parameters and create wrapper in db
                            Create record entity with given parameters:
                            :param identifier: int identifier of book, like 1, 2, 3 or ...
                            :param book_name: name of the book to include
                            :param book_category: category of the book, like math or programming
                            :param read_date: date when book was read.
                            :param book_type: type of the book, can contain one of the value - audio or text.
                            """
                            self.id = identifier
                            self.book_name = book_name
                            self.book_category = book_category
                            self.read_date = read_date
                            self.type = book_type

                        def get_book_id(self):
                            return self.id

                        def get_book_name(self):
                            return self.book_name

                        def get_dir_name(self):
                            return self.book_category

                        def get_read_date(self):
                            return self.read_date

                        def get_book_type(self):
                            return self.type

                        def print_object(self):
                            print(f'''
                            Book name: {self.book_name},
                            Book category: {self.book_category},
                            Book read date: {self.read_date}
                            ''')

                    def __init__(self, table_name: str):
                        self.table_name = table_name
                        self.__inner_table: list = list()  # inner table container for records
                        # initialize table and create file
                        self.__init_table()

                    def get_table_name(self):
                        return self.table_name

                    @cancelable_operation
                    def add_record(self, record):
                        try:
                            self.__inner_table.append(record)
                        except Exception as e:
                            print(f'An exception during add record to table - {e}')

                    @cancelable_operation
                    def update_record(self, table_name: str, identifier: str):
                        pass

                    @cancelable_operation
                    def delete_record(self, table_name: str, identifier: str):
                        pass

                    @log
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

                __tables: list[_Table]  # container for tables in database

                def __init__(self, database_name: str):
                    self.database_name: str = database_name
                    self.__tables = list()
                    if not os.listdir().__contains__(database_name):
                        self.__init_database()
                    else:
                        pass

                def __find_table(self, predicate) -> _Table:
                    """
                    Inner method of finding table in database.
                    :param predicate: predicate function for comparison, should take _Table object and return bool value.
                    :return: Table object that equals predicate.
                    """
                    table_to_return = None
                    if isinstance(predicate, types.FunctionType):
                        for table in self.__tables:
                            if predicate(table):
                                table_to_return = table
                                break
                        return table_to_return
                    else:
                        raise DatabaseException(f'Given predicate {predicate} is not a function')

                @cancelable_operation
                def _create_table(self, table_name: str) -> None:
                    """
                    Creates new file, called table in terms of book database.
                    :return: None
                    """
                    try:
                        new_table = self._Table(table_name)
                        self.__tables.append(new_table)
                    except Exception as e:
                        print(f'An exception occurred during creating table - {e}')

                @cancelable_operation
                def _delete_table(self, table_name: str) -> None:
                    if not len(self.__tables):
                        self.__tables.remove(self.__find_table(lambda x: x.get_table_name() == table_name))
                    else:
                        raise DatabaseException(f'Error during deleting table with given name {table_name}')

                def get_tables(self):
                    if not len(self.__tables) == 0:
                        return self.__tables
                    else:
                        raise DatabaseException('')

                @log
                def __init_database(self):
                    """
                    Create database and initialize database architecture by creating folders (tables)
                    :return:
                    """
                    pass

            def __init__(self):
                self.databases: list = list()

            @cancelable_operation
            def _create_database(self, db_name: str) -> None:
                try:
                    new_database = self._Database(db_name)
                    self.databases.append(new_database)
                except Exception as e:
                    print()

            @cancelable_operation
            def synchronize(self) -> None:
                """
                Method for synchronizing e-book files and database tables
                :return: None
                """
                pass

            @log
            def get_database(self):
                if len(self.databases) != 0:
                    return self.databases
                else:
                    raise

        def __int__(self):
            # Interpreter entities init:
            self.database_core = self._Database_core()

        @log
        def parse_sentence(self, sentence: str) -> None:
            """
            Parse given sentence in book query language and invoke functions.
            :param sentence: string sentence in book query language.
            :return: None
            """
            lexemes = sentence.split(' ')
            operator = lexemes[0].lower()  # operator name in lower case, so you can write in UPPER or lower case
            if operator in self.__syntax_rules.keys():  # check if operator contains in syntax rules
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
                        raise SyntaxInterpreterException(
                            f'Unknown operator given - {operator}'
                        )  # yeah, I know that I handle this problem
            else:
                raise SyntaxInterpreterException('Sentence should start with one of the operators')

        @log
        def __parse_select_operator(self, lexemes: list[str]):
            pass

        @log
        def __parse_delete_operator(self, lexemes: list[str]):
            pass

        @log
        def __parse_create_operator(self, lexemes: list[str]):
            pass

        @log
        def __parse_update_operator(self, lexemes: list[str]):
            pass

        @log
        def __parse_add_operator(self, lexemes: list[str]):
            pass

        @log
        def __parse_sync_operator(self):
            self.database_core.synchronize()

        @log
        def print_help(self):
            print('This module is responsible for database functionality')
            print('Here are words that used')
            for _, value in self.__syntax_rules:
                print(f'{value[0]} word contains next comment: {value[1]}')

    def __init__(self, is_interactive_mode: bool = None, start_point: str | PathLike = '.'):
        self.is_interactive = is_interactive_mode
        self.syntax_interpreter = self.Syntax_interpreter()
        self.start_point = start_point

    @staticmethod
    def __get_table_view(file_descriptor) -> list[str]:
        """
        Read all lines from database and return list with lines
        :param file_descriptor: file descriptor to use
        :return: list with lines (records)
        """
        return file_descriptor.readlines()

    @log
    def __run_interactive(self):
        while True:
            print('Enter command to run in interpreter or "close" to close: ', end='')
            user_command_line = input()
            if user_command_line != '':
                if user_command_line != 'close':
                    self.syntax_interpreter.parse_sentence(user_command_line)
                else:
                    print('Close cli connection to database')
                    break
            else:
                print('Entered empty command, try again')
                continue

    @log
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
                print(f'An error during non interactive mode execution - {e}')

    @log
    def run_module(self) -> None:
        """
        Main entry point to database actions module.
        Can be interactive (in cli by BQL (book query language)) or just pick commands from list
        :return: None
        """
        try:
            if self.is_interactive is None:
                while True:
                    choice = str_input_from_user('Run module interactively or not?')
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
