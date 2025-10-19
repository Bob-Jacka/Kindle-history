"""
Kindle history module
Store your read books in file or delete already read book from your e-book, like Kindle

Module gives you an interactive way of using your e-book
"""

try:
    from core.entities.BotLogger import BotLogger
    from core.entities.Formatter import Format
    from enum import Enum

    from core.entities.AbstractModule import Module, INPUT_SYM, CLOSE_MENU_CODE

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
        TextIO, Final, re
    )
except Exception as e:
    print(f'An exception occurred during dependencies import - {e}')

###########Main logic of the app

# App paths:
central_dir: str
"""
directory address where app stored (home directory)
"""

current_dir: str
"""
pointer to current working directory of the application
"""

path_to_books_dir: str
"""
path where your books stored
"""

book_read_file: str
"""
Alias name for path where stored file with books history
"""

FULL_PATH_TO_READ_FILE: str
"""
Alias variable name for central dir + file name with read books
"""

global_logger: BotLogger
"""
Global instance of logger class.
Change logger parameter to turn on logs in console.
Logger creates in different branches of app execution.
"""


class Book_data:
    """
    Class for encapsulating book data.
    Include dir where book stored and its name.
    """

    __SAVE_POINT_EXTENSION: Final[str] = '.sdr'
    """
    Extension of the file with bookmarks in cracked Kindle device. 
    """

    def __init__(self, current_working_dir: str | os.PathLike = '.', book_name: str = ''):
        self.current_dir = current_working_dir
        self.book_name = book_name

    def get_current_dir(self) -> str:
        return self.current_dir

    def get_book_name(self) -> str:
        return self.book_name

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
        return self.current_dir + self.book_name[:self.book_name.find('.')] + self.__SAVE_POINT_EXTENSION

    def get_save_point_name(self) -> str:
        """
        Method for retrieving name with save point dir extension.
        Do not exception safe, need to check path before use.
        :return: name of bookmark dir
        """
        return self.book_name[:self.book_name.find('.')] + self.__SAVE_POINT_EXTENSION

    def has_bookmark_dir(self) -> bool:
        """
        Method for checking if bookmark dir exists
        :return: bool value of existence.
        """
        return Path(self.book_name[:self.book_name.find('.')] + self.__SAVE_POINT_EXTENSION).exists()

    def get_lua_data(self) -> tuple[bool, float, str]:
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
            global_logger.log(f'Exception while getting path to lua script - {e}')

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
                    global_logger.log('Print lua script lines')
                    for line in all_file:
                        print(line)
                else:
                    global_logger.log('Return lua script lines')
                    return all_file
        except Exception as e:
            global_logger.log(f'Exception while getting path to lua script - {e}')


class Strategy(ABC):
    """
    Virtual class for app strategy
    """

    def __init__(self, local_logger: BotLogger):
        self.__STATIC_FILE_NAME_WITH_READ: Final[str] = '../../data/read.txt'
        """
        Static file name where you store your statistics about books that you already read.
        """
        self.fs_util = Fs_utility(self.get_static_file_with_red())
        self.fs_util.open_read_file()
        self.local_logger: BotLogger = local_logger

    def init_app(self) -> None:
        """
        Main entry point to app.
        Initialize some useful application variables.
        Contains in base class for strategies
        :return: None
        """
        global current_dir, central_dir, book_read_file, FULL_PATH_TO_READ_FILE
        try:
            central_dir = os.getcwd()
            current_dir = os.getcwd()
            FULL_PATH_TO_READ_FILE = central_dir + os.path.sep + self.__STATIC_FILE_NAME_WITH_READ
            if os.path.exists(FULL_PATH_TO_READ_FILE):
                global_logger.log('Read books file found')
                book_read_file = os.path.join(central_dir, self.__STATIC_FILE_NAME_WITH_READ)
            else:
                global_logger.log('Read books file not found')
                Format.prYellow('Would you like to create file with read books? (yes(y) /no (n))')
                user_choice = input(INPUT_SYM)
                if user_choice == 'yes' or user_choice == 'y':
                    os.mknod(central_dir + os.sep + self.get_static_file_with_red())
                    book_read_file = os.path.join(central_dir, self.__STATIC_FILE_NAME_WITH_READ)
                    global_logger.log('File for your book history created!')
                else:
                    global_logger.log('Read file not found and create, app closing')
                    exit(1)
            global_logger.log('App initialized with paths in manual mode')
            if current_dir is None:
                global_logger.log('Current directory cannot be None.')
                raise Exception('Current directory cannot be None.')
        except Exception as e:
            global_logger.log(f'Some exception occurred in init app - {e}')
            exit(1)

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

    def set_local_logger(self, logger: BotLogger):
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
        global current_dir
        while True:
            print(f'Your current path is - "{Format.underline_start + current_dir + Format.underline_end}"')
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
                            current_dir = central_dir
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
                            self.fs_util.count_books()
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
        print(f'Home directory - {central_dir},')
        print(f'Current app directory - {current_dir},')
        print(f'File with read books - {book_read_file is not None if 'Book file exist' else 'No path given'},')
        print(
            f'File extensions of books - {'txt', 'fb2', 'epub', 'pdf', 'doc', 'docx', 'rtf', 'mobi', 'kf8', 'azw', 'lrf', 'djvu'}')
        print('Ways to use this app:')
        print('1. Use with config')
        print('2. Use without config - manually choose auto or manual mode for application work.')
        while True:
            print('Would you like to see help for config file - yes (y) or no (n)?')
            user_input = input(INPUT_SYM)
            if user_input == 'yes' or user_input == 'y':
                Fs_utility.App_config.get_help_config()
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

    def __init__(self, local_logger: BotLogger = None):
        super().__init__(local_logger)

    @override
    def do_algorithm(self):
        """
        Main cycle of auto strategy
        :return: None
        """
        self.init_app()
        while True:
            print(f'Your current path is - "{Format.underline_start + current_dir + Format.underline_end}"')
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
                        book = Book_data(current_dir, book_file)
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

    def __init__(self, local_logger: BotLogger = None):
        super().__init__(local_logger)

    @override
    def do_algorithm(self):
        """
        Main cycle of manual strategy
        :return: None
        """
        self.init_app()
        while True:
            print(f'Your current path is - "{Format.underline_start + current_dir + Format.underline_end}"')
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
                            self.__list_all_read_book(current_dir)
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
            print(f'Your current path is - "{Format.underline_start + current_dir + Format.underline_end}"')
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
                            self.move_upper()
                            break
                        case 2:
                            self.move_lower()
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

    @staticmethod
    def move_upper():
        """
        Move upper in file system tree
        :return: None
        """
        global current_dir
        current_dir = Path(current_dir).parent

    @staticmethod
    def move_lower():
        """
        Move lower in file system tree
        :return: None
        """
        global current_dir
        p = Path('../..')  # check current directory
        dir_list = [x for x in p.iterdir() if x.is_dir()]
        Format.prGreen('Available directories:')
        if len(dir_list) == 0:
            Format.prRed('There are no directories nearby')
        else:
            dir_counter = 0  # change value to zero if you are a programmer.
            for dir in dir_list:
                print(f'{dir_counter}: {dir.name}')
                dir_counter += 1

            print()  # just empty line
            print(f'Or {CLOSE_MENU_CODE}: to exit this menu')

            while True:
                print('Enter dir number to move in')
                dir_number = int(input(INPUT_SYM))
                if dir_number in range(len(dir_list)):
                    current_dir = dir_list[dir_number].as_posix()
                    break
                elif dir_number == int(CLOSE_MENU_CODE):
                    global_logger.log('Close menu')
                    break

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
                                current_working_dir=current_dir + os.sep,
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
        fav_books = os.listdir(central_dir)
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


class Fs_utility:
    """
    Class for file systems actions.
    """

    config_name: str = 'config'
    """
    Static name of the config file
    """

    class EBookManufacturer(Enum):
        """
        Enum with several e-book manufacturers
        """
        kindle = 'kindle',
        onyx = 'onyx'
        pocket_book = 'pocket_book'

    class OSType(Enum):
        windows_os = 'Windows',
        linux_os = 'Linux',
        mac_os = 'Mac_os'

    def __init__(self, file_with_read: str | os.PathLike):
        self.path_to_read_file = file_with_read
        self.file_with_read_book = None
        self.__BOOK_EXTENSIONS: list[str] = ['txt', 'fb2', 'epub', 'pdf', 'doc', 'docx', 'rtf', 'mobi', 'kf8', 'azw',
                                             'lrf', 'djvu']
        """
        Extensions of the books to be located by listing all files in directory.
        """

    def close_read_file(self):
        try:
            self.file_with_read_book.close()
        except Exception as e:
            global_logger.log(f'Exception occurred while closing file with read books - {e}')

    def open_read_file(self):
        try:
            self.file_with_read_book = open(self.path_to_read_file)
        except Exception as e:
            global_logger.log(f'Exception occurred while opening file with read books - {e}')
            self.file_with_read_book.close()

    def is_book(self, name: str) -> bool:
        """
        Function for filtering directory for books
        :param name: name of the file to proceed
        :return: bool value, if name ended with 'book' extensions.
        """
        for ext in self.__BOOK_EXTENSIONS:
            if name.endswith(ext):
                return True
        else:
            return False

    def do_backup_copy(self) -> None:
        """
        Function for backup your books in given directory (Download dir).
        :return: None
        """
        global_logger.log('Backup books invoked')
        save_path: str | os.PathLike
        if platform.system() == Fs_utility.OSType.windows_os:
            save_path = Path.home().as_uri() + os.sep + 'Downloads'
            global_logger.log('Windows user path to Downloads')
        elif platform.system() == Fs_utility.OSType.linux_os:
            save_path = Path.home().as_uri() + os.sep + 'Downloads'
            global_logger.log('Linux user path to Downloads')
        else:
            raise Exception('Unknown operating system, not implemented yet.')

        for dir in os.listdir(central_dir):
            self.copy_fs_entity(dir, save_path)
            global_logger.log(f'File - {dir} backed up in {save_path}')

    def reset_data(self) -> None:
        """
        Method for deleting all book data (exclude file with book read).
        Also home directory of the app will be saved.
        :return: None
        """
        while True:
            print('Do you really want to delete all books data? yes (y) or no (n)')
            user_choice = input(INPUT_SYM)
            if user_choice == 'yes' or user_choice == 'y':
                global_logger.log('Reset data is invoked')
                dir_list = self.get_book_data_dirs_list()
                for dir in dir_list:
                    self.delete_fs_entity(dir)
            elif user_choice == 'no' or user_choice == 'n':
                global_logger.log('Reset data canceled')
            else:
                print('Wrong choice, try again')
                continue

    @staticmethod
    def get_book_data_dirs_list() -> list:
        """
        Method for receiving book data (directories names with books, except home directory)
        :return: list with strings (paths)
        """
        lst = os.listdir(Path('../../..'))  # go back, out of home directory.
        if central_dir in lst:
            global_logger.log('Central dir removed from lst in get book data list')
            lst.remove(central_dir)
        else:
            global_logger.log('Central dir is not in lst')
        return lst

    def delete_fs_entity(self, path: str | os.PathLike) -> None:
        """
        Function for deleting book in given path, also can delete directory with save points;
        :param path: path to book
        :return: None
        """
        global_logger.log('Delete fs entity invoked')
        if path is not None:

            # file branch
            if os.path.isfile(path):
                try:
                    if path.endswith(self.path_to_read_file):
                        global_logger.log('You cannot delete your read file!')
                    else:
                        os.remove(path)
                        Format.prGreen('Book deleted from directory')
                except Exception as e:
                    global_logger.log(f'Exception occurred in deleting book in {path} - {e}')

            # directory branch
            elif os.path.isdir(path):
                try:
                    shutil.rmtree(path)
                    Format.prGreen(f'Directory {path} deleted')
                except Exception as e:
                    global_logger.log(f'Exception occurred in deleting directory in {path} - {e}')
        else:
            global_logger.log('Path cannot be None')

    def copy_fs_entity(self, path: str | os.PathLike, dir_name: str = '') -> None:
        """
        Save your book in central directory (app installation home).
        :param path: path from where you want to copy read book.
        :param dir_name: *optional parameter, special for directory copying. Use for creating new directory and copy all into
        :return: None
        """
        global_logger.log('Copy fs entity invoked')
        if path is not None:

            # file branch
            if os.path.isfile(path):
                try:
                    shutil.copy2(path, central_dir)  # {src} {dest}
                    Format.prGreen('Book save in central directory')
                except Exception as e:
                    global_logger.log(f'Error occurred while saving book in central dir - {e}')

            # directory branch
            elif os.path.isdir(path):
                try:
                    new_save_point_path = central_dir + os.sep + dir_name
                    os.mkdir(new_save_point_path)  # create new directory, instead of deleting old
                    shutil.copytree(path, new_save_point_path, dirs_exist_ok=True)  # {src} {dest}
                    Format.prGreen('Directory save in central directory')
                except Exception as e:
                    global_logger.log(f'Error occurred while saving directory in central dir - {e}')

            else:
                Format.prRed('Object type nor file or directory')
                raise Exception(f'Cannot determine object type of {path}')
            self.delete_fs_entity(path)
        else:
            global_logger.log('Path cannot be None')

    def creation_date(self, path_to_file: str | os.PathLike) -> str:
        """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
        """
        if platform.system() == Fs_utility.OSType.windows_os:
            return str(os.path.getctime(path_to_file))
        elif platform.system() == Fs_utility.OSType.linux_os:
            try:
                mtime = os.path.getmtime(path_to_file)
                mtime_readable = datetime.date.fromtimestamp(mtime)
                return str(mtime_readable)
            except AttributeError:
                return str(datetime.datetime.now())
        else:
            raise NotImplemented('It seems that you have Mac operating system, not implemented for this system')

    @staticmethod
    def is_need_for_new_line() -> bool:
        """
        Super dummy function for checking if you need new line symbol in read file.
        :return: bool value if you need for new line in read file
        """
        books_counter: int = 0
        new_line_counter: int = 0
        with open(FULL_PATH_TO_READ_FILE, 'r') as book_file:
            while True:
                line = book_file.readline()

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

    @staticmethod
    def find_book() -> None:
        """
        Function for finding book in read file, by providing book name or name part.
        :return: None
        """
        while True:
            Format.prYellow('Enter book name to find')
            book_to_find = input(INPUT_SYM)
            if book_to_find != '' and book_to_find is not None:
                with open(FULL_PATH_TO_READ_FILE) as book_file:
                    for book in book_file:
                        if book.find(book_to_find):
                            Format.prGreen('Book found')
                            break
                        else:
                            Format.prRed('Book not found')
                            break
                    break  # exit loop if book found or not

    def get_file_with_read(self):
        """
        Getter method for read book file descriptor
        :return:
        """
        return self.file_with_read_book

    def count_books(self):
        """
        Function for count books in read file if exists
        :return: book count in terminal
        """
        if os.path.exists(self.path_to_read_file):
            book_counter = 0
            for line in self.file_with_read_book:
                if line != '\n':
                    book_counter += 1
            print(f'Books count is - {Format.underline_start + str(book_counter) + Format.underline_end}')

        else:
            global_logger.log('Read book file not found!')

    class App_config:
        """
        Class for configuration application with parameters.
        Simple store variables app configuration.
        """

        __read_book_file: str
        """
        Name of the file with read book.
        """

        __is_auto_mode: bool
        """
        Is auto resolve books.
        """

        __is_enable_logs: bool
        """
        Is logs in application enabled.
        """

        __exclude_directories: list[str]
        """
        Which directories to ignore by app.
        Contains string objects.
        """

        def __init__(self, ):
            self.__read_book_file = ''
            self.__is_auto_mode = False
            self.__is_enable_logs = False
            self.__exclude_directories = list()

        @staticmethod
        def get_help_config() -> None:
            print('App config help.')
            print('Config can contain next parameters:')
            print('1. read_book_file_name - name of the file with read books,')
            print('2. is_auto_mode - turn on by default auto mode in application,')
            print('3. is_enable_logs - turn on of off logs in application,')
            print('4. exclude_directories - which directories to ignore by book search.')
            print('How to write config file:')
            print('Write in config file next lines')

            print('read_book_file_name: <your file name>')
            print('is_auto_mode: <true or false values>')
            print('is_enable_logs: <true or false values>')
            print('exclude_directories: <one_dir_name, second_dir_name, third_dir_name> (list with dirs names)')
            if not os.path.exists(Fs_utility.config_name):
                global_logger.log('Config is not exits')
                while True:
                    print('Would you like to create test config file in this directory - yes (y) or no (n)?')
                    user_input = input(INPUT_SYM)
                    if user_input == 'yes' or user_input == 'y':
                        Fs_utility.App_config.create_tmp_config()
                        break
                    else:
                        break

        def init_config(self, config_file_name: str) -> None:
            """
            Initialize app by given config.
            :param config_file_name: name of the config file to init.
            :return: None
            """
            with open(config_file_name) as file:
                for line in file:
                    if ':' in line:
                        split_line = line.split(':')
                        if line.startswith('read_book_file_name'):
                            self.__read_book_file = split_line[1]
                        elif line.startswith('is_auto_mode'):
                            self.__is_auto_mode = bool(split_line[1])
                        elif line.startswith('exclude_directories'):
                            self.__exclude_directories = list(split_line[1])
                        else:
                            raise Exception(f'Wrong config parameter - {line}')
                    else:
                        raise Exception(f'Wrong config parameter - {line}')
                else:
                    raise Exception('Exception in checking lines')

        def get_read_file_name(self):
            if self.__read_book_file is not None:
                return self.__read_book_file
            else:
                raise Exception('Try to get null value')

        def get_is_auto_mode(self):
            if self.__is_auto_mode is not None:
                return self.__is_auto_mode
            else:
                raise Exception('Try to get null value')

        def get_is_global_enable_log(self):
            """
            Return bool value is global logs enabled
            :return:
            """
            if self.__is_enable_logs is not None:
                return self.__is_enable_logs
            else:
                raise Exception('Try to get null value')

        def get_exclude_dirs(self):
            if self.__exclude_directories is not None:
                return self.__exclude_directories
            else:
                raise Exception('Try to get null value')

        @staticmethod
        def create_tmp_config():
            """
            Creates config if you cannot do it by yourself.
            :return: None
            """
            try:
                with open(Fs_utility.config_name, 'w+') as tmp_config:
                    tmp_config.write('read_book_file_name: read.txt')
                    tmp_config.write('\n')
                    tmp_config.write('is_auto_mode: false')
                    tmp_config.write('\n')

                    tmp_config.write('is_enable_logs: false')
                    tmp_config.write('\n')
                    tmp_config.write('exclude_directories: None')
                    tmp_config.write('\n')
                global_logger.log('Config file created successfully')
            except Exception as e:
                print(f'Exception in create config file - {e}')


####################Tests
class Kindle_history_test:
    """
    Class for testing app.
    Include unit tests for testing app for bugs or undefined behavior
    """

    def __init__(self):
        print('Test class do test actions')
        self.fs_util = Fs_utility(FULL_PATH_TO_READ_FILE)

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
            global_logger = BotLogger(is_on=False)
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
        elif len(cli_args) == 2 and cli_args[1].startswith(f'--{Fs_utility.config_name}'):  # check for config flag
            cur_dir = os.listdir(Path('../..').absolute())
            config: Fs_utility.App_config | None = None
            if Fs_utility.config_name in cur_dir:
                config_num = cur_dir.index(Fs_utility.config_name)
                config = Fs_utility.App_config()
                config.init_config(cur_dir[config_num])
                if config.get_is_global_enable_log():
                    global_logger = BotLogger(is_on=True)  # logs appear in console
                else:
                    global_logger = BotLogger(is_on=False)  # logs cannot appear in console
                global_logger.log('Config file founded')
                if config.get_is_auto_mode():
                    strat = AutoStrategy()
                else:
                    strat = ManualStrategy()
                strat.do_algorithm()  # execute strategy
                strat.fs_util.close_read_file()
            else:
                raise Exception('Wrong config declaration, config not found')

        else:
            raise Exception('I do not know, how you start app, but exception.')

        print('Bye')
