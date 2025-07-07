"""
Kindle history
Store your read books in file or delete already read book from your e-book, like Kindle

Utility gives you an interactive way of using your e-book
"""

import datetime
import os
import shutil
from pathlib import Path


class Format:
    """
    Utility class for text formater
    """
    underline_end = '\033[0m'
    underline_start = '\033[4m'

    @staticmethod
    def prRed(string):
        print("\033[91m {}\033[00m".format(string))

    @staticmethod
    def prGreen(string):
        print("\033[92m {}\033[00m".format(string))

    @staticmethod
    def prYellow(string):
        print("\033[93m {}\033[00m".format(string))

    @staticmethod
    def prCyan(string):
        print("\033[96m {}\033[00m".format(string))

    @staticmethod
    def prLightGray(string):
        print("\033[97m {}\033[00m".format(string))


###########Main logic of the app

# App settings:
APP_VERSION = '1.1.0'
"""
Simple version of the app
"""

STATIC_FILE_NAME_WITH_READ = 'read.txt'
"""
Static file name where you store your statistics about books that you already read.
"""

BOOK_EXTENSIONS: list[str] = ['txt', 'fb2', 'epub', 'pdf', 'doc', 'docx', 'rtf', 'mobi', 'kf8', 'azw', 'lrf', 'djvu']
"""
Extensions of the books to be located by listing all files in directory.
"""

CLOSE_MENU_CODE = '666'
"""
Code for close menu functionality
"""

# App paths:
central_dir: str  # directory address where app stored
current_dir: str  # pointer to current working directory of the application
path_to_books_dir: str  # path where your books

book_read_file: str  # path to file where stored read books


def _is_book(name: str) -> bool:
    """
    Function for filtering directory for books
    :param name:
    :return:
    """
    for ext in BOOK_EXTENSIONS:
        if name.endswith(ext):
            return True
        else:
            return False


def list_all_read_book(path):
    """
    Function for output all books that have been red.
    outputs only files with books extensions.
    :param path:
    :return: None
    """
    if path is not None:
        files = os.listdir(path)
        filtered_list = list(filter(_is_book, files))  # list with only books
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
                book_num = int(input('>> '))
                if book_num in range(len(filtered_list) + 1):
                    book_name = filtered_list[book_num]  # name of the book to delete / save
                    add_new_book(current_dir + os.path.sep + book_name, book_name)
                    break
                elif book_num == 666:
                    Format.prYellow('Close menu')
                    break
    else:
        Format.prRed('Path cannot be null')


def count_books():
    """
    Function for count books in read file if exists
    :return: book count in terminal
    """
    path_to_read_file = central_dir + os.path.sep + STATIC_FILE_NAME_WITH_READ
    if os.path.exists(path_to_read_file):
        book_counter = 0
        with open(path_to_read_file) as file:
            for line in file:
                if line != '\n':
                    book_counter += 1
        print(f'Books count is - {Format.underline_start + str(book_counter) + Format.underline_end}')
    else:
        Format.prRed('Read book file not found!')


def book_delete(path):
    """
    Function for deleting book in given path;
    :param path: path to book
    :return: None
    """
    try:
        if path.endswith(STATIC_FILE_NAME_WITH_READ):
            Format.prRed('You cannot delete your read file!')
        else:
            os.remove(path)
            Format.prGreen('Book deleted')
    except Exception as e:
        Format.prRed(f'Exception occurred in deleting book in {path} - {e}')


def add_new_book(path, book_name: str):
    """
    :param book_name: name of the book to add
    :param path: full path to the list with read books
    :return: None
    """
    if path is not None:
        try:
            with open(central_dir + os.path.sep + f'{STATIC_FILE_NAME_WITH_READ}', 'a') as book_file:
                if STATIC_FILE_NAME_WITH_READ is not None:
                    book_file.write('\n')  # add new line before
                    book_file.write(book_name + ' - ' + str(datetime.date.today()))  # write into file with read books
                    Format.prGreen('Add new book')
                    while True:  # slice book name for better read in console
                        print(
                            f'Do you want to save "{Format.underline_start}{book_name[0: 80]}{Format.underline_end}" in your central directory?')
                        print('yes (y) / no (n)')
                        user_input = input('>> ')
                        if user_input == 'yes' or user_input == 'y':
                            move_book(path)
                            break
                        elif user_input == 'no' or user_input == 'n':
                            book_delete(path)  # delete book if you not want to
                            break
                        else:
                            continue  # continue if user is so dummy, give him another chance!
                else:
                    book_delete(path)
        except Exception as e:
            Format.prRed(f'Exception while adding new book - {e}')


def move_book(path):
    """
    Save your book in central directory (app installation home)
    :param path: path from where you want to copy read book
    :return: None
    """
    if path is not None:
        try:
            shutil.copy(path, central_dir)  # {src} {dest}
        except Exception as e:
            Format.prRed(f'Error occurred while saving book in central dir - {e}')
        Format.prGreen('Book save in central directory')
        book_delete(path)
    else:
        Format.prRed('Path cannot be None')


def print_help():
    """
    Standard help function
    :return: help words to poor user
    """
    print('Kindle history app')
    print(f'App version - {Format.underline_start + APP_VERSION + Format.underline_end}')
    print('Instruction:')
    print('1) To use this app - place it in directory with books that you already read.')
    print('2) Move to your dir where you want to move your')
    print('3) Choose action with book')
    print('* You can save your book or just add this book to read list')
    print(f'''
    **You need to include file with name - "{STATIC_FILE_NAME_WITH_READ}" in dir 
    where you contain this app to write read book to the list.
    '''
          )


def init_app():
    """
    Main entry point to app.
    Initialize some useful application variables.
    :return: None
    """
    global current_dir, central_dir, book_read_file
    try:
        central_dir = os.getcwd()
        current_dir = os.getcwd()
        if os.path.exists(central_dir + os.path.sep + f'{STATIC_FILE_NAME_WITH_READ}'):
            Format.prGreen('Read books file found')
            book_read_file = os.path.join(central_dir, STATIC_FILE_NAME_WITH_READ)
        else:
            Format.prRed('Read books file not found')
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
        print(f'{CLOSE_MENU_CODE}: to exit this menu')

        while True:
            print('Enter dir number to move in')
            dir_number = int(input('>> '))
            if dir_number in range(len(dir_list)):
                current_dir = dir_list[dir_number].as_posix()
                break
            elif dir_number == 666:
                Format.prYellow('Close menu')
                break


if __name__ == '__main__':
    init_app()
    while True:
        print(f'Your current path is - "{Format.underline_start + current_dir + Format.underline_end}"')
        Format.prYellow('Available actions:')
        print('1) Move upper')
        print('2) Move lower')
        print('3) List all files (only books files) in directory...')
        print('4) Go home')

        print('5) Help')
        print('6) Count books')

        print('7) Exit app')
        Format.prYellow('Choose action by entering number')
        try:
            act_num: int = int(input('>> '))
            if act_num in range(1, 8):
                match act_num:
                    case 1:
                        move_upper()
                    case 2:
                        move_lower()
                    case 3:
                        list_all_read_book(current_dir)
                    case 4:
                        current_dir = central_dir
                        Format.prGreen('Path changed')
                    case 5:
                        print_help()
                    case 6:
                        count_books()
                    case 7:
                        Format.prCyan('Out app')
                        exit(0)
                    case _:
                        Format.prRed('Wrong choice, try again!')
                        continue
                print()
        except Exception as e:
            Format.prRed(f'Exception occurred in Main cycle of the program - {e}')
            exit(1)
