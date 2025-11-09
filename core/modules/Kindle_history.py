"""
Kindle history module
Store your read books in file or delete already read book from your e-book, like Kindle

Module gives you an interactive way of using your e-book
"""
try:
    from core.entities.App_config import (
        App_config,
        _config_name
    )
    from core.entities.Kindle_history_entities.Book_data import Book_data
    from core.entities.File_controller import File_controller
    from core.entities.PathFinder import (
        get_central_dir_name,
        get_current_dir_name,
        set_current_dir,
        move_upper,
        move_lower,
        count_books
    )
    from data.Constants import (
        global_logger,
        INPUT_SYM,
        CLOSE_MENU_CODE
    )

    from core.entities.Formatter import Format
    from enum import Enum

    from core.entities.AbstractModule import Module

    import datetime
    import inspect
    import os
    import platform
    import shutil
    import sys
    from abc import (
        ABC,
        abstractmethod
    )
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


class Strategy(ABC):
    """
    Virtual class for app strategy
    """

    def __init__(self, local_logger):
        self.__STATIC_FILE_NAME_WITH_READ: Final[str] = '../../testData/read.txt'
        """
        Static file name where you store your statistics about books that you already read.
        """
        self.fs_util = File_controller()
        self.local_logger = local_logger

    def get_static_file_with_red(self) -> str:
        """
        Method for returning name of the static file where stored all read book.
        :return: str value of file name.
        """
        return self.__STATIC_FILE_NAME_WITH_READ

    def get_local_logger(self):
        """
        None safety get local logger method
        :return: Bot logger entity
        """
        if self.local_logger is not None:
            return self.local_logger
        else:
            global_logger.log("Local logger is None")

    def set_local_logger(self, logger):
        """
        None safety set local logger method
        :return: None
        """
        if logger is not None:
            self.local_logger = logger
        else:
            global_logger.log("Logger is None")

    def app_settings_menu(self) -> None:
        """
        Menu with app settings.
        :return: None
        """
        while True:
            print(f'Your current path is - "{Format.underline_start + get_current_dir_name() + Format.underline_end}"')
            Format.prYellow('Available actions in app settings:')
            print('1) Go home path')
            print('2) Change file with already read books')
            print('3) Count books in read file')
            print('4) Print app help')
            print('5) Backup books in Download directory')
            print('6) Reset book data...')
            print('7) Close menu')
            try:
                act_num: int = int(input(INPUT_SYM))
                if act_num in range(1, 8):  # from 1 to 4
                    match act_num:
                        case 1:
                            set_current_dir(get_central_dir_name())
                            Format.prGreen('Path changed')
                        case 2:
                            new_name = input('Input new name, >> ')
                            if new_name is not None:
                                __STATIC_FILE_NAME_WITH_READ = new_name
                                Format.prGreen(f'Name, where stored file with books changed to {new_name}')
                                break
                            else:
                                Format.prRed('Wrong new name or empty, try again')
                                continue
                        case 3:
                            count_books()
                        case 4:
                            self.print_help()
                        case 5:
                            self.fs_util.do_backup_copy()
                        case 6:
                            self.fs_util.reset_data()
                        case 7:
                            break
                        case _:
                            Format.prRed('Wrong choice')
                            continue
            except Exception as e:
                global_logger.log(f'Exception occurred in settings - {e}.')
                exit(1)

    def print_help(self):
        """
        Standard help function
        :return: help words to poor user
        """
        print('Kindle history app')
        print('Instruction:')
        print('1) To use this app - place it in directory with books that you already read.')
        print('2) Move to your dir where you want to move your')
        print('3) Choose action with book')
        print(f'*You need to include file with name - "{self.__STATIC_FILE_NAME_WITH_READ}" in dir ')
        print('where you contain this app to write read book to the list.')
        print('Some useful app variables:')
        print(f'Home directory - {get_central_dir_name()},')
        print(f'Current app directory - {get_current_dir_name()},')
        print(f'File with read books - {book_read_file is not None if 'Book file exist' else 'No path given'},')
        print('Ways to use this app:')
        print('1. Use with config')
        print('2. Use without config - manually choose auto or manual mode for application work.')
        while True:
            print('Would you like to see help for config file - yes (y) or no (n)?')
            user_input = input(INPUT_SYM)
            if user_input == 'yes' or user_input == 'y':
                App_config.get_help_config()
                break
            else:
                break

    @abstractmethod
    def do_algorithm(self):
        pass

    @abstractmethod
    def add_new_book(self, book: Book_data):
        pass


class AutoStrategy(Strategy):
    """
    Derived class from Strategy.
    Responsible for automation of book deletion and saving.
    """

    def __init__(self, local_logger=None):
        super().__init__(local_logger)

    @override
    def do_algorithm(self):
        """
        Main cycle of auto strategy
        :return: None
        """
        while True:
            print(f'Your current path is - "{Format.underline_start + get_current_dir_name() + Format.underline_end}"')
            Format.prYellow('Available actions:')
            print('1) Start auto process')
            print('2) App setting...')
            print('3) Exit app')
            Format.prYellow('Choose action by entering number')
            try:
                act_num: int = int(input(INPUT_SYM))
                if act_num in range(1, 4):  # from 1 to 3 (not 4)
                    match act_num:
                        case 1:
                            self.__auto_process_books()
                        case 2:
                            self.app_settings_menu()
                        case 3:
                            print('Out app, bye!')
                            exit(0)
                        case _:
                            Format.prRed('Wrong choice, try again')
                            continue
                    print()  # simple space after menu
            except Exception as e:
                global_logger.log(f'Exception occurred in Main cycle of the program - {e}')
                exit(1)

    @override
    def add_new_book(self, book: Book_data) -> None:
        """
        Add new book for auto processing.
        :param book: book object to add
        :return: None
        """
        if book is not None:
            try:
                book_name: str  # name of the book to proceed
                if self.__STATIC_FILE_NAME_WITH_READ is not None:
                    if self.fs_util.is_need_for_new_line():
                        self.fs_util.file_with_read_book.write('\n')  # add new line before

                    if len(book.get_book_name()) > 80:  # write only first 80 symbols of book name
                        book_name = copy(book.get_book_name())[0:80] + '...'
                    else:
                        book_name = copy(book.get_book_name())  # do not cut book name

                    self.fs_util.file_with_read_book.write(
                        book_name + ' - ' + str(self.fs_util.creation_date(book.get_full_path())))
                    self.fs_util.copy_fs_entity(book.get_full_path())
                    self.fs_util.copy_fs_entity(book.get_save_point_path(),
                                                dir_name=book.get_save_point_name())
                    global_logger.log('Save points also saved')
                    self.fs_util.delete_fs_entity(
                        book.get_full_path())  # delete book if you not want to save it
                else:
                    self.fs_util.delete_fs_entity(book.get_full_path())

            except Exception as e:
                global_logger.log(f'Exception while adding new book - {e}')

    def __auto_process_books(self, path_to_process='..') -> None:
        """
        Main method of the auto strategy class.
        :param path_to_process: path where to start processing, by default equal to double dot
        :return: None
        """
        p = Path(path_to_process)  # move out of read directory to global files
        global_dir = p.iterdir()
        dirs_list: list = list()
        if global_dir is not None:
            global_logger.log(f"Use path - {global_dir}")
            for entry in global_dir:  # add entries if directory. All directories with books
                if entry.is_dir():
                    dir_entry = entry.absolute().__str__()
                    dirs_list.append(dir_entry)  # append directory to proceed later
                    global_logger.log(f"Directory added - {dir_entry}")
                else:
                    global_logger.log(f'Entry is file - {entry}')

            for dir_name in dirs_list:  # process directories in global_dir
                for book_file in dir_name:  # process books files in directory
                    if self.fs_util.is_book(book_file):
                        global_logger.log(f'Found book file ({book_file}) in directory ({dir_name})')
                        book = Book_data(get_current_dir_name(), book_file)
                        if book.has_bookmark_dir():
                            global_logger.log(f'Found bookmark directory, decide to add book - {book.get_book_name()}')
                            if Book_data.decide_if_book_finished(book.get_lua_data()):
                                global_logger.log('Book really finished')
                                self.add_new_book(book)
                            else:
                                global_logger.log(
                                    f'Book is not finished truly, go read it or change book status to finished - {book.get_book_name()}')
                                del book
                        else:
                            global_logger.log('Book add cancel, no bookmark dir found')
                    else:
                        global_logger.log('Given book file is not a book')
            else:
                pass
        else:
            global_logger.log("Global directory is None")


class ManualStrategy(Strategy):
    """
    Derived class from Strategy.
    Responsible for manual mode of the app.
    """

    def __init__(self, local_logger=None):
        super().__init__(local_logger)

    @override
    def do_algorithm(self):
        """
        Main cycle of manual strategy
        :return: None
        """
        while True:
            print(f'Your current path is - "{Format.underline_start + get_current_dir_name() + Format.underline_end}"')
            Format.prYellow('Available actions:')
            print('1) Move menu...')
            print('2) App setting...')
            print('3) List all files (only books files) in directory')
            print('4) List favourite books (in home directory)')
            print('5) Exit app')
            Format.prYellow('Choose action by entering number')
            try:
                act_num: int = int(input(INPUT_SYM))
                if act_num in range(1, 6):  # from 1 to 5 (not 6)
                    match act_num:
                        case 1:
                            self.__move_menu()
                        case 2:
                            self.app_settings_menu()  # derived from Strategy
                        case 3:
                            self.__list_all_read_book(get_current_dir_name())
                        case 4:
                            self.__list_favourite_books()
                        case 5:
                            print('Out app, bye!')
                            exit(0)
                        case _:
                            Format.prRed('Wrong choice, try again')
                            continue
                    print()  # simple space after menu
            except Exception as e:
                global_logger.log(f'Exception occurred in Main cycle of the program - {e}')
                exit(1)

    def __move_menu(self):
        """
        Main menu with actions
        :return: None
        """
        while True:
            print(f'Your current path is - "{Format.underline_start + get_current_dir_name() + Format.underline_end}"')
            Format.prYellow('Available actions in app settings:')
            print('1) Move upper')
            print('2) Move lower')
            print('3) Find book')
            print('4) Close menu')
            try:
                act_num: int = int(input(INPUT_SYM))
                if act_num in range(1, 5):  # from 1 to 5
                    match act_num:
                        case 1:
                            move_upper()
                            break
                        case 2:
                            move_lower()
                            break
                        case 3:
                            self.fs_util.find_book()
                        case 4:
                            break
                        case _:
                            Format.prRed('Wrong choice, try again')
                            continue
                    print()
            except Exception as e:
                global_logger.log(f'Exception occurred in settings - {e}.')
                exit(1)

    def __list_all_read_book(self, path: str | os.PathLike):
        """
        Function for output all books that have been red.
        outputs only files with books extensions.
        :param path: path to directory, which is listed
        :return: None
        """

        if path is not None:
            files = os.listdir(path)
            filtered_list = list(filter(self.fs_util.is_book, files))  # list with only books
            if self.get_static_file_with_red() in filtered_list:
                filtered_list.remove(self.get_static_file_with_red())  # remove file with read books
            print('All books in file:')
            if len(filtered_list) == 0:
                print('There are no books in directory')
            else:
                book_file_counter = 0  # first value of the output dir
                for file in filtered_list:
                    print(f'{Format.underline_start + str(book_file_counter) + Format.underline_end}: {file}')
                    book_file_counter += 1
                print()  # just add new line after books
                print(f'{Format.underline_start + CLOSE_MENU_CODE + Format.underline_end}: to exit this menu')
                while True:
                    Format.prYellow('Choose book to finish reading, enter number')
                    book_num = int(input(INPUT_SYM))
                    if book_num in range(len(filtered_list) + 1):
                        book_name = filtered_list[book_num]  # name of the book to delete / save
                        self.add_new_book(
                            Book_data(
                                current_storing_dir=get_current_dir_name() + os.sep,
                                book_name=book_name
                            )
                        )
                        break
                    elif book_num == int(CLOSE_MENU_CODE):
                        Format.prYellow('Close menu')
                        break
        else:
            global_logger.log('Path cannot be null')

    def __list_favourite_books(self):
        """
        Function for listing favourite books (books that saved in home directory)
        :return: None
        """
        fav_books = os.listdir(get_central_dir_name())
        fav_filtered_list = list(filter(self.fs_util.is_book, fav_books))
        fav_filtered_list.remove(self.get_static_file_with_red())  # because we list home dir, there will be read.txt
        if len(fav_filtered_list) != 0:
            fav_book_counter = 0
            for fav_book in fav_filtered_list:
                print(f'{fav_book_counter}. {fav_book}')
                fav_book_counter += 1
        else:
            print('There are no favourite or just simple books!')

    @override
    def add_new_book(self, book_data: Book_data):
        """
        :param book_data: tuple with book info, where first argument is path to book and second argument is book name
        :return: None
        """
        if book_data is not None:
            try:
                book_name: str  # name of the book to proceed
                if self.__STATIC_FILE_NAME_WITH_READ is not None:
                    if self.fs_util.is_need_for_new_line():
                        self.fs_util.file_with_read_book.write('\n')  # add new line before
                    if len(book_data.get_book_name()) > 80:  # write only first 80 symbols of book name
                        book_name = copy(book_data.get_book_name())[0:80] + '...'
                    else:
                        book_name = copy(book_data.get_book_name())  # do not cut book name
                    self.fs_util.file_with_read_book.write(
                        book_name + ' - ' + str(self.fs_util.creation_date(book_data.get_full_path())))
                    while True:  # slice book name for better read in console
                        print(
                            f'Do you want to save "{Format.underline_start}{book_name}{Format.underline_end}" (and save points) in your central directory?')
                        print('yes (y) / no (n)')  # ask user if user want to save book and save point in book
                        user_input = input(INPUT_SYM)
                        if user_input == 'yes' or user_input == 'y':
                            self.fs_util.copy_fs_entity(book_data.get_full_path())
                            if os.path.exists(book_data.get_save_point_path()):  # Also save bookmarks if exists
                                self.fs_util.copy_fs_entity(book_data.get_save_point_path(),
                                                            dir_name=book_data.get_save_point_name())
                                global_logger.log('Save points also saved')
                            break
                        elif user_input == 'no' or user_input == 'n':
                            self.fs_util.delete_fs_entity(
                                book_data.get_full_path())  # delete book if you not want to save it
                            break
                        else:
                            continue  # continue if user is so dummy, give him another chance!
                else:
                    self.fs_util.delete_fs_entity(book_data.get_full_path())
            except Exception as e:
                global_logger.log(f'Exception while adding new book - {e}')


####################Tests
class Kindle_history_test:
    """
    Class for testing app.
    Include unit tests for testing app for bugs or undefined behavior
    """

    def __init__(self):
        print('Test class do test actions')

    def test_delete_book1(self):
        self.fs_util.delete_fs_entity('')

    def test_delete_book2(self):
        self.fs_util.delete_fs_entity('')

    def test_move_book(self):
        self.fs_util.copy_fs_entity('')

    def test_move_directory(self):
        self.fs_util.copy_fs_entity('')

    def test_format_class1(self):
        Format.prRed('Hello world')

    def test_format_class2(self):
        Format.prYellow('Hello world')

    def test_format_class3(self):
        Format.prGreen('Hello world')

    def test_format_class4(self):
        Format.prCyan('Hello world')

    def test_format_class5(self):
        Format.prLightGray('Hello world')

    def test_init_app(self):
        pass

    def test_fs_get_book_data_dirs(self):
        print(self.fs_util.get_book_data_dirs_list())


class Kindle_history(Module):

    def run_module(self):
        """
        Run kindle history module
        :return: None
        """
        cli_args = sys.argv  # get cli arguments

        # Manual or auto branch to execute:
        if len(cli_args) == 1:  # run without arguments
            del cli_args
            strat: Strategy | None = None
            Format.prYellow('Auto mode - yes (y) or no (n):')
            while True:
                mode_user_input = str(input(INPUT_SYM))
                if mode_user_input is not None:
                    if mode_user_input == 'yes' or mode_user_input == 'y':
                        strat = AutoStrategy()
                        break
                    elif mode_user_input == 'no' or mode_user_input == 'n':
                        strat = ManualStrategy()
                        break
                    else:
                        Format.prRed('Wrong choice, try again')
                        continue
                else:
                    Format.prRed('Not received user input')
                    exit(1)
            try:
                strat.do_algorithm()  # execute strategy
                strat.fs_util.close_read_file()
            except Exception as e:
                global_logger.log(f'Error occurred in main logic start algorithm - {e}')

        # Test branch to execute:
        elif len(cli_args) == 2 and cli_args[1] == 'test':  # static name of the test mode
            test_class = Kindle_history_test()
            methods = [name for name, value in
                       inspect.getmembers(Kindle_history_test, inspect.isfunction) if
                       name != '__init__']  # turn on test mode

            for method in methods:
                getattr(test_class, method)

        # Config branch to execute:
        elif len(cli_args) == 2 and cli_args[1].startswith(f'--{_config_name}'):  # check for config flag
            cur_dir = os.listdir(Path('../..').absolute())
            config: App_config | None = None
            if _config_name in cur_dir:
                config_num = cur_dir.index(_config_name)
                config = App_config()
                config.init_config(cur_dir[config_num])
                global_logger.log('Config file founded')
                if config.get_is_auto_mode():
                    strat = AutoStrategy()
                else:
                    strat = ManualStrategy()
                strat.do_algorithm()  # execute strategy
            else:
                raise Exception('Wrong config declaration, config not found')

        else:
            raise Exception('I do not know, how you start app, but exception.')

        print('Bye')
