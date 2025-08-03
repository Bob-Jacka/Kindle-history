"""
Kindle history
Store your read books in file or delete already read book from your e-book, like Kindle

Utility gives you an interactive way of using your e-book
"""
import datetime
import inspect
import os
import platform
import shutil
import sys
from copy import copy
from pathlib import Path


####################Tests
class Kindle_history_test:
    """
    Class for testing app.
    Include unit tests for testing app for bugs or undefined behavior
    """

    def __init__(self):
        print('Test class do test actions')

    def test_delete_book1(self):
        delete_fs_entity('')

    def test_delete_book2(self):
        delete_fs_entity('')

    def test_move_book(self):
        move_fs_entity('')

    def test_move_directory(self):
        move_fs_entity('')

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
        init_app()


####################


class Format:
    """
    Utility class for text formater
    Includes print functions in different colors and underline technology.
    """
    underline_end = '\033[0m'
    underline_start = '\033[4m'

    @staticmethod
    def prRed(string: str):
        print("\033[91m {}\033[00m".format(string))

    @staticmethod
    def prGreen(string: str):
        print("\033[92m {}\033[00m".format(string))

    @staticmethod
    def prYellow(string: str):
        print("\033[93m {}\033[00m".format(string))

    @staticmethod
    def prCyan(string: str):
        print("\033[96m {}\033[00m".format(string))

    @staticmethod
    def prLightGray(string: str):
        print("\033[97m {}\033[00m".format(string))


###########Main logic of the app

# App settings:
__APP_VERSION = '1.6.0'
"""
Simple version of the app
"""

__STATIC_FILE_NAME_WITH_READ = 'read.txt'
"""
Static file name where you store your statistics about books that you already read.
"""

__BOOK_EXTENSIONS: list[str] = ['txt', 'fb2', 'epub', 'pdf', 'doc', 'docx', 'rtf', 'mobi', 'kf8', 'azw', 'lrf', 'djvu']
"""
Extensions of the books to be located by listing all files in directory.
"""

CLOSE_MENU_CODE = '666'
"""
Code for close menu functionality
"""

INPUT_SYM = '>> '
"""
Symbol that applies in input fields
"""

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


class Book_data:
    """
    Class for encapsulating book data
    """

    __SAVE_POINT_EXTENSION: str = '.sdr'
    """
    Extension of the file with bookmarks in cracked Kindle device. 
    """

    def __init__(self, current_dir: str | os.PathLike, book_name: str):
        self.current_dir = current_dir
        self.book_name = book_name

    def get_current_dir(self) -> str:
        return self.current_dir

    def get_book_name(self) -> str:
        return self.book_name

    def get_book_extension(self) -> str:
        """
        Receives book extension by cutting book name
        :return: string value for book extension
        """
        global __BOOK_EXTENSIONS
        copy_book_name = copy(self.book_name)
        book_ext = copy_book_name[-1:copy_book_name.find('.')]
        if book_ext in __BOOK_EXTENSIONS:
            return book_ext
        else:
            Format.prRed('Book extension does not support')

    def get_full_path(self) -> str:
        """
        Method for returning full path by concatenating current dir and book name
        :return: string value
        """
        return self.current_dir + self.book_name

    def get_save_point_path(self) -> str:
        """
        Method for returning path to save points.
        Do not exception safe, need to check path before use
        :return: string value
        """
        return self.current_dir + self.book_name[:self.book_name.find('.')] + self.__SAVE_POINT_EXTENSION

    def get_save_point_name(self):
        """
        Method for retrieving name with save point dir extension.
        Do not exception safe, need to check path before use
        :return:
        """
        return self.book_name[:self.book_name.find('.')] + self.__SAVE_POINT_EXTENSION


def _is_book(name: str) -> bool:
    """
    Function for filtering directory for books
    :param name: name of the file to proceed
    :return: bool value, if name ended with 'book' extension.
    """
    for ext in __BOOK_EXTENSIONS:
        if name.endswith(ext):
            return True


def list_favourite_books():
    """
    Function for listing favourite books (books that saved in home directory)
    :return: None
    """
    fav_books = os.listdir(central_dir)
    fav_filtered_list = list(filter(_is_book, fav_books))
    fav_filtered_list.remove(__STATIC_FILE_NAME_WITH_READ)  # because we list home dir, there will be read.txt
    if len(fav_filtered_list) != 0:
        fav_book_counter = 0
        for fav_book in fav_filtered_list:
            print(f'{fav_book_counter}. {fav_book}')
            fav_book_counter += 1
    else:
        print('There are no favourite or just simple books!')


def count_books():
    """
    Function for count books in read file if exists
    :return: book count in terminal
    """
    if os.path.exists(FULL_PATH_TO_READ_FILE):
        book_counter = 0
        with open(FULL_PATH_TO_READ_FILE) as file:
            for line in file:
                if line != '\n':
                    book_counter += 1
        print(f'Books count is - {Format.underline_start + str(book_counter) + Format.underline_end}')
    else:
        Format.prRed('Read book file not found!')


def delete_fs_entity(path: str | os.PathLike):
    """
    Function for deleting book in given path, also can delete directory with save points;
    :param path: path to book
    :return: None
    """
    if path is not None:
        if os.path.isfile(path):
            try:
                if path.endswith(__STATIC_FILE_NAME_WITH_READ):
                    Format.prRed('You cannot delete your read file!')
                else:
                    os.remove(path)
                    Format.prGreen('Book deleted from directory')
            except Exception as e:
                Format.prRed(f'Exception occurred in deleting book in {path} - {e}')

        elif os.path.isdir(path):
            try:
                shutil.rmtree(path)
                Format.prGreen('Directory deleted')
            except Exception as e:
                Format.prRed(f'Exception occurred in deleting directory in {path} - {e}')
    else:
        Format.prRed('Path cannot be None')


def move_fs_entity(path: str | os.PathLike, dir_name: str = ''):
    """
    Save your book in central directory (app installation home)
    :param path: path from where you want to copy read book
    :param dir_name: *optional parameter, special for directory copying. Use for creating new directory and copy all into
    :return: None
    """
    if path is not None:
        if os.path.isfile(path):
            try:
                shutil.copy2(path, central_dir)  # {src} {dest}
                Format.prGreen('Book save in central directory')
            except Exception as e:
                Format.prRed(f'Error occurred while saving book in central dir - {e}')

        elif os.path.isdir(path):
            try:
                new_save_point_path = central_dir + os.sep + dir_name
                os.mkdir(new_save_point_path)  # create new directory, instead of deleting old
                shutil.copytree(path, new_save_point_path, dirs_exist_ok=True)  # {src} {dest}
                Format.prGreen('Directory save in central directory')
            except Exception as e:
                Format.prRed(f'Error occurred while saving directory in central dir - {e}')

        else:
            Format.prRed('Object type nor file or directory')
            raise Exception(f'Cannot determine object type of {path}')
        delete_fs_entity(path)
    else:
        Format.prRed('Path cannot be None')


def list_all_read_book(path: str | os.PathLike):
    """
    Function for output all books that have been red.
    outputs only files with books extensions.
    :param path: path to directory, which is listed
    :return: None
    """
    if path is not None:
        files = os.listdir(path)
        filtered_list = list(filter(_is_book, files))  # list with only books
        if __STATIC_FILE_NAME_WITH_READ in filtered_list:
            filtered_list.remove(__STATIC_FILE_NAME_WITH_READ)  # remove file with read books
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
                    add_new_book(
                        Book_data(
                            current_dir=current_dir + os.sep,
                            book_name=book_name
                        )
                    )
                    break
                elif book_num == int(CLOSE_MENU_CODE):
                    Format.prYellow('Close menu')
                    break
    else:
        Format.prRed('Path cannot be null')


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return str(os.path.getctime(path_to_file))
    elif platform.system() == 'Linux':
        try:
            mtime = os.path.getmtime(path_to_file)
            mtime_readable = datetime.date.fromtimestamp(mtime)
            return str(mtime_readable)
        except AttributeError:
            return str(datetime.datetime.now())
    else:
        pass


def is_need_for_new_line() -> bool:
    """
    Super dummy function
    :return: bool value if need for new line in read file
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


def add_new_book(book_data: Book_data):
    """
    :param book_data: tuple with book info, where first argument is path to book and second argument is book name
    :return: None
    """
    if book_data is not None:
        try:
            with open(FULL_PATH_TO_READ_FILE, 'a') as read_book_file:
                book_name: str  # name of the book to proceed
                if __STATIC_FILE_NAME_WITH_READ is not None:
                    if is_need_for_new_line():
                        read_book_file.write('\n')  # add new line before
                    if len(book_data.get_book_name()) > 80:  # write only first 80 symbols of book name
                        book_name = copy(book_data.get_book_name())[0:80] + '...'
                    else:
                        book_name = copy(book_data.get_book_name())  # do not cut book name
                    read_book_file.write(book_name + ' - ' + str(creation_date(book_data.get_full_path())))
                    while True:  # slice book name for better read in console
                        print(
                            f'Do you want to save "{Format.underline_start}{book_name}{Format.underline_end}" (and save points) in your central directory?')
                        print('yes (y) / no (n)')  # ask user if user want to save book and save point in book
                        user_input = input(INPUT_SYM)
                        if user_input == 'yes' or user_input == 'y':
                            move_fs_entity(book_data.get_full_path())
                            if os.path.exists(book_data.get_save_point_path()):  # Also save bookmarks if exists
                                move_fs_entity(book_data.get_save_point_path(),
                                               dir_name=book_data.get_save_point_name())
                                Format.prGreen('Save points also saved')
                            break
                        elif user_input == 'no' or user_input == 'n':
                            delete_fs_entity(book_data.get_full_path())  # delete book if you not want to save it
                            break
                        else:
                            continue  # continue if user is so dummy, give him another chance!
                else:
                    delete_fs_entity(book_data.get_full_path())
        except Exception as e:
            Format.prRed(f'Exception while adding new book - {e}')


def print_help():
    """
    Standard help function
    :return: help words to poor user
    """
    print('Kindle history app')
    print(f'App version - {Format.underline_start + __APP_VERSION + Format.underline_end}')
    print('Instruction:')
    print('1) To use this app - place it in directory with books that you already read.')
    print('2) Move to your dir where you want to move your')
    print('3) Choose action with book')
    print(f'''
    *You need to include file with name - "{__STATIC_FILE_NAME_WITH_READ}" in dir 
    where you contain this app to write read book to the list.
    Some useful app variables:
        Home directory - {central_dir},
        Current app directory - {current_dir},
        File with read books - {book_read_file is not None if 'Book file exist' else 'No path given'},
        File extensions of books - {__BOOK_EXTENSIONS}
    '''
          )


def init_app():
    """
    Main entry point to app.
    Initialize some useful application variables.
    :return: None
    """
    global current_dir, central_dir, book_read_file, FULL_PATH_TO_READ_FILE
    try:
        central_dir = os.getcwd()
        current_dir = os.getcwd()
        FULL_PATH_TO_READ_FILE = central_dir + os.path.sep + __STATIC_FILE_NAME_WITH_READ
        if os.path.exists(FULL_PATH_TO_READ_FILE):
            Format.prGreen('Read books file found')
            book_read_file = os.path.join(central_dir, __STATIC_FILE_NAME_WITH_READ)
        else:
            Format.prRed('Read books file not found')
            Format.prYellow('Would you like to create file with read books? (yes(y) /no (n))')
            user_choice = input(INPUT_SYM)
            if user_choice == 'yes' or user_choice == 'y':
                os.mknod(central_dir + os.sep + __STATIC_FILE_NAME_WITH_READ)
                book_read_file = os.path.join(central_dir, __STATIC_FILE_NAME_WITH_READ)
                Format.prGreen('File for your book history created!')
            # raise Exception('With read books not found') # uncomment this line if you want you exit from app
        Format.prGreen('App initialized with paths')
        if current_dir is None:
            raise Exception('Current directory cannot be None.')
    except Exception as e:
        Format.prRed(f'Some exception occurred in init app - {e}')
        exit(1)


def move_upper():
    """
    Move upper in file system tree
    :return: None
    """
    global current_dir
    current_dir = Path(current_dir).parent


def move_lower():
    """
    Move lower in file system tree
    :return: None
    """
    global current_dir
    p = Path('.')  # check current directory
    dir_list = [x for x in p.iterdir() if x.is_dir()]
    Format.prGreen('Available directories:')
    if len(dir_list) == 0:
        Format.prRed('There are no directories nearby')
    else:
        dir_counter = 0  # change value to zero if you are programmer
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
                Format.prYellow('Close menu')
                break


def app_settings_menu():
    """
    Menu with app settings
    :return:
    """
    global __STATIC_FILE_NAME_WITH_READ, current_dir
    while True:
        print(f'Your current path is - "{Format.underline_start + current_dir + Format.underline_end}"')
        Format.prYellow('Available actions in app settings:')
        print('1) Go home path')
        print('2) Change file with already read books')
        print('3) Print app help')
        print('4) Close menu')
        try:
            act_num: int = int(input(INPUT_SYM))
            if act_num in range(1, 5):  # from 1 to 4
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
                        print_help()
                    case 4:
                        break
                    case _:
                        Format.prRed('Wrong choice')
                        continue
        except Exception as e:
            Format.prRed(f'Exception occurred in settings - {e}.')
            exit(1)


def find_book():
    """
    Function for finding book in read file.
    :return: None
    """
    while True:
        Format.prYellow('Enter book name to find')
        book_to_find = input(INPUT_SYM)
        if book_to_find != '' and book_to_find is not None:
            with open(FULL_PATH_TO_READ_FILE) as book_file:
                for book in book_file:
                    if book.find(book_to_find):
                        Format.prRed('Book found')
                        break
                    else:
                        Format.prGreen('Book not found')
                        break
                break  # exit loop if book found or not


def action_menu():
    """
    Main menu with actions
    :return: None
    """
    while True:
        print(f'Your current path is - "{Format.underline_start + current_dir + Format.underline_end}"')
        Format.prYellow('Available actions in app settings:')
        print('1) Move upper')
        print('2) Move lower')
        print('3) Count books')
        print('4) Find book')
        print('5) Close menu')
        try:
            act_num: int = int(input(INPUT_SYM))
            if act_num in range(1, 6):  # from 1 to 4
                match act_num:
                    case 1:
                        move_upper()
                        break
                    case 2:
                        move_lower()
                        break
                    case 3:
                        count_books()
                    case 4:
                        find_book()
                    case 5:
                        break
                    case _:
                        Format.prRed('Wrong choice')
                        continue
                print()
        except Exception as e:
            Format.prRed(f'Exception occurred in settings - {e}.')
            exit(1)


if __name__ == '__main__':
    cli_args = sys.argv  # get cli arguments
    if len(cli_args) == 1:
        init_app()
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
                if act_num in range(1, 6):  # from 1 to 6
                    match act_num:
                        case 1:
                            action_menu()
                        case 2:
                            app_settings_menu()
                        case 3:
                            list_all_read_book(current_dir)
                        case 4:
                            list_favourite_books()
                        case 5:
                            print('Out app, bye!')
                            exit(0)
                        case _:
                            Format.prRed('Wrong choice, try again')
                            continue
                    print()  # simple space after menu
            except Exception as e:
                Format.prRed(f'Exception occurred in Main cycle of the program - {e}')
                exit(1)
    elif len(cli_args) == 2 and cli_args[1] == 'test':  # static name of the test mode
        test_class = Kindle_history_test()
        methods = [name for name, value in
                   inspect.getmembers(Kindle_history_test, inspect.isfunction) if
                   name != '__init__']  # turn on test mode

        for method in methods:
            getattr(test_class, method)
