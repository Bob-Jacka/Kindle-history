""""
Entry point to utility and modules, contains global data from modules
"""

import os

from core.entities.Formatter import Format
from core.entities.browser.Web_interface import Web_interface
from core.entities.console.App_config import App_config
from core.modules.Book_db import Book_db
from core.modules.Kindle_history import Kindle_history
from core.modules.Settings import Setting
from core.modules.Transfer_book import Transfer_book
from core.other.Utils import (
    int_input_from_user,
    str_input_from_user
)
from data.Constants import (
    INPUT_SYM,
    APP_NAME,
    STATIC_CONFIG_NAME,
    STATIC_READ_FILE_NAME
)
from data.Wrappers import log


class BootLoader:

    def __init__(self):
        self.app_config = None
        self.logger = None

        self.init_app()

        self.history_module: Kindle_history
        # Kindle_history(app_config=self.app_config, readFile=self.app_config.get_read_file_name(), cli_parameters=list())

    @log
    def run_app_console(self):
        """
        Run application in console interface
        :return: None
        """
        while True:
            print('Enter module number to use it:')
            print('1. Kindle history module - to change your read file')
            print('2. Transfer book - to transfer your books from pc to e-book')
            print('3. Book database module - to manage your books saved on e-book')
            print('4. Settings')

            print('5. Help')
            print('6. Exit - to exit from utility')
            module_to_use = int_input_from_user(values_range=6)
            match module_to_use:
                case 1:
                    self.history_module.run_module()
                case 2:
                    transfer_module = Transfer_book(app_config=self.app_config)
                    transfer_module.run_module()
                case 3:
                    book_db = Book_db(app_config=self.app_config)
                    book_db.run_module()
                case 4:
                    settings = Setting(app_config=self.app_config)
                case 5:
                    self.help_distribution_manager()
                    continue
                case 6:
                    break
                case _:
                    print('Wrong module number, try again')
                    continue

    @log
    def run_app_browser(self):
        """
        Run application in browser
        :return: None
        """
        webinterface = Web_interface()
        webinterface.run_interface()

    @log
    def help_distribution_manager(self):
        print(f'{APP_NAME} utility')
        print('Description:')
        print('You can manage your saved books with help of this utility.')
        print('')
        print('')
        print('')
        print('')

    @staticmethod
    def read_config_file() -> App_config | None:
        user_input = str_input_from_user('Enter new config file name')
        try:
            with open(user_input, 'r') as config_file:

                config_to_return = App_config()
                for line in config_file:
                    pass
        except Exception as e:
            print(f'Exception during config file read - {e}')

    def init_app(self) -> None:
        """
        Main entry point to app.
        Initialize some useful application variables.
        Contains in base class for strategies
        :return: None
        """
        try:
            print('Check for config file in files directory by default name')
            if not os.path.exists(App_config.get_real_path(STATIC_CONFIG_NAME)):
                self.app_config = App_config()
                self.logger = self.app_config.get_logger()
                self.logger.log('Config file not found, using default values in configuration')
            else:
                self.app_config = self.read_config_file()

            self.logger.log(f'App initialized in "{self.app_config.get_central_dir_name()}" path in filesystem')
            self.logger.log('Checking for file with read file by default name')
            if os.path.exists(STATIC_READ_FILE_NAME):
                self.logger.log('Read books file found')
            else:
                self.logger.log('Read books file not found')
                Format.prYellow('Would you like to create file with read books? (yes(y) /no (n))')
                user_choice = input(INPUT_SYM)
                if user_choice == 'yes' or user_choice == 'y':
                    os.mknod(self.app_config.get_central_dir_name() + os.sep + STATIC_READ_FILE_NAME)
                    self.logger.log('File for your book history created!')
                else:
                    self.logger.log('Read file not found or create, app closing')
                    exit(1)
            self.logger.log('App initialized in manual mode')
            if self.app_config.get_current_dir_name() is None:
                self.logger.log('Current directory cannot be None.')
                raise Exception('Current directory cannot be None.')
        except Exception as e:
            self.logger.log(f'Some exception occurred in init app - {e}')
            exit(1)

#################################################################################
