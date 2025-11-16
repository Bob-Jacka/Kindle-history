""""
Entry point to utility and modules, contains global data from modules
"""
import os

from core.entities.App_config import App_config
from core.entities.Formatter import Format
from core.modules.Book_db import Book_db
from core.modules.Kindle_history import Kindle_history
from core.modules.Transfer_book import Transfer_book
from data.Constants import (
    STATIC_FILE_NAME_WITH_READ,
    INPUT_SYM
)


class Distribution_manager:

    def __init__(self):
        self.app_config = None
        self.logger = None

    def run_app(self):
        self.init_app()
        while True:
            print('Enter module number to use it')
            print('1. Kindle history module - to store your read books')
            print('2. Transfer book - to transfer your books from pc to e-book')
            print('3. Book database module - to access database functionality inside utility')
            print('4. Exit - to exit from utility')
            module_to_use = int(input('>> '))
            match module_to_use:
                case 1:
                    history_module = Kindle_history(self.app_config, self.app_config.get_read_file_name())
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

    def help_distribution_manager(self):
        pass

    def init_app(self) -> None:
        """
        Main entry point to app.
        Initialize some useful application variables.
        Contains in base class for strategies
        :return: None
        """
        try:
            self.app_config = App_config()

            if os.path.exists(self.app_config.get_read_file_name()):
                self.logger.log('Read books file found')
            else:
                self.logger.log('Read books file not found')
                Format.prYellow('Would you like to create file with read books? (yes(y) /no (n))')
                user_choice = input(INPUT_SYM)
                if user_choice == 'yes' or user_choice == 'y':
                    os.mknod(self.app_config.get_central_dir_name() + os.sep + STATIC_FILE_NAME_WITH_READ)
                    self.logger.log('File for your book history created!')
                else:
                    self.logger.log('Read file not found and create, app closing')
                    exit(1)
            self.logger.log('App initialized with paths in manual mode')
            if self.app_config.get_current_dir_name() is None:
                self.logger.log('Current directory cannot be None.')
                raise Exception('Current directory cannot be None.')
        except Exception as e:
            self.logger.log(f'Some exception occurred in init app - {e}')
            exit(1)


if __name__ == '__main__':
    Distribution_manager().run_app()
