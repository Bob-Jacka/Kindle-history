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

*Module is only responsible for books on your e-book
"""

from core.entities.console.AbstractModule import Module
from core.entities.console.Database_entities.BQL_core import Syntax_interpreter
from core.other.Utils import str_input_from_user
from data.Constants import INPUT_SYM
from data.Wrappers import log


class Book_db(Module):
    """
    Custom nosql database for storing information about books on your e-book
    """

    def __init__(self, app_config):
        self.__is_interactive = app_config.get_is_auto_mode()
        self.__syntax_interpreter = Syntax_interpreter()
        self.__start_point = app_config.get_central_dir_name()
        self.__local_logger = app_config.get_logger()

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
        self.__local_logger.log('Run interactive mode')
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
                self.__local_logger.log('Entered empty command, try again')
                continue

    @log
    def __run_non_interactive(self):
        self.__local_logger.log('Run non interactive mode')
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
                self.__local_logger.log(f'An error during non interactive mode execution - {e}')

    @log
    def run_module(self) -> None:
        """
        Main entry point to database actions module.
        Can be interactive (in cli by BQL (book query language)) or just pick commands from list
        :return: None
        """
        try:
            if self.__is_interactive is None:
                while True:
                    choice = str_input_from_user('Run module interactively or not?')
                    if choice == 'yes':
                        self.__run_interactive()
                        break
                    else:
                        self.__run_non_interactive()
                        break
            else:
                if self.__is_interactive:
                    self.__run_interactive()
                else:
                    self.__run_non_interactive()
        except Exception as e:
            print(f'An exception in run module method - {e}')
