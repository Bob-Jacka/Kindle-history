"""
Module for small, inner Nosql database for books and book actions.
Contains CRUD action list for using and some special syntax to use interactive

                    Module architecture:
                        run_module
                        /           \
            __run_interactive     __run_non_interactive
                    |
                parse_sentence
(parse sentence one lexeme by one)

"""

import enum
from os import PathLike
from typing import (
    Final
)

from core.entities.AbstractModule import Module
from core.entities.Database_entities.Database import _Database
from core.exceptions.DatabaseException import (
    SyntaxInterpreterException
)
from core.other.Utils import str_input_from_user
from data.Constants import INPUT_SYM
from data.Wrappers import (
    cancelable_operation,
    log
)


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
                Order of execution:
            1. first you need to create database object
            2. second create tables in your database
            3. and last create records in tables
            4. And fourth, use it...
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
            'using': tuple(('using', 'use this word for use database as a main database')),

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

        def __int__(self):
            # Interpreter entities init:
            self.databases: list = list()

        @cancelable_operation
        def _create_database(self, db_name: str) -> None:
            try:
                new_database = _Database(db_name)
                self.databases.append(new_database)
            except Exception as e:
                print(f'An exception occurred while creating database - {e}')

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

        @log
        def parse_sentence(self, sentence: str) -> None:
            """
            Parse given sentence in book query language and invoke functions.
            :param sentence: string sentence in book query language.
            :return: None
            """
            lexemes = sentence.split(' ')  # split input string with whitespace
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
            self.synchronize()

        @log
        def print_help(self):
            print('This module is responsible for database functionality')
            print('Here are words that used')
            for _, value in self.__syntax_rules:
                print(f'{value[0]} word contains next comment: {value[1]}')

    def __init__(self, is_interactive_mode: bool = None, start_point: str | PathLike = '.'):
        self.is_interactive = is_interactive_mode
        self.__syntax_interpreter = self.Syntax_interpreter()
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
                    self.__syntax_interpreter.parse_sentence(user_command_line)
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
                user_command_number: int = int(input(INPUT_SYM))
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
