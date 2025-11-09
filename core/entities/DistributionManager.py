""""
Entry point to utility and modules, contains global data from modules
"""
import os

from core.entities.Formatter import Format
from core.entities.PathFinder import (
    set_fullpath_to_readfile,
    get_fullpath_to_readfile
)
from core.modules.Book_db import Book_db
from core.modules.Kindle_history import Kindle_history
from core.modules.Transfer_book import Transfer_book
from data.Constants import (
    global_logger,
    STATIC_FILE_NAME_WITH_READ,
    INPUT_SYM
)


def help_distribution_manager():
    pass


def init_app() -> None:
    """
    Main entry point to app.
    Initialize some useful application variables.
    Contains in base class for strategies
    :return: None
    """
    try:
        central_dir = os.getcwd()
        current_dir = os.getcwd()
        set_fullpath_to_readfile(central_dir + os.path.sep + STATIC_FILE_NAME_WITH_READ)
        if os.path.exists(get_fullpath_to_readfile()):
            global_logger.log('Read books file found')
        else:
            global_logger.log('Read books file not found')
            Format.prYellow('Would you like to create file with read books? (yes(y) /no (n))')
            user_choice = input(INPUT_SYM)
            if user_choice == 'yes' or user_choice == 'y':
                os.mknod(central_dir + os.sep + STATIC_FILE_NAME_WITH_READ)
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


if __name__ == '__main__':
    init_app()
    while True:
        print('Enter module number to use it')
        print('1. Kindle history module - to store your read books')
        print('2. Transfer book - to transfer your books from pc to e-book')
        print('3. Book database module - to access database functionality inside utility')
        print('4. Exit - to exit from utility')
        module_to_use = int(input('>> '))
        match module_to_use:
            case 1:
                history_module = Kindle_history()
                history_module.run_module()
            case 2:
                transfer_module = Transfer_book()
                transfer_module.run_module()
            case 3:
                book_db = Book_db()
                book_db.run_module()
            case 4:
                print('Bye')
                exit(0)
            case _:
                print('Wrong module number, try again')
                continue
