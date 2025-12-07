""""
Entry point to utility and modules, contains global data from modules
"""

import os

from core.entities.browser.Web_module import Web_interface
from core.modules.Book_db import Book_db
from core.modules.Kindle_history import Kindle_history
from core.modules.Settings import Setting
from core.modules.Transfer_book import Transfer_book
from core.other.Utils import (
    int_input_from_user
)
from data.Constants import (
    APP_NAME
)
from data.Wrappers import log


class BootLoader:

    def __init__(self, app_config, logger):
        self.app_config = app_config
        self.local_logger = logger

        self.history_module: Kindle_history = Kindle_history(cli_parameters=list())
        self.book_db_module: Book_db = Book_db()
        self.transfer_module: Transfer_book = Transfer_book()
        self.settings_module: Setting = Setting()

    def init_app_entities(self):
        self.history_module.post_init(self.app_config)
        self.book_db_module.post_init(self.app_config)
        self.settings_module.post_init(self.app_config)
        self.transfer_module.post_init(self.app_config)

    @log
    def run_app_console(self):
        """
        Run application in console interface
        :return: None
        """
        self.init_app_entities()
        try:
            self.local_logger.log(f'Console process run on pid {os.getpid()}')
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
                        self.transfer_module.run_module()
                    case 3:
                        self.book_db_module.run_module()
                    case 4:
                        self.settings_module.run_module()
                    case 5:
                        self.help_distribution_manager()
                        continue
                    case 6:
                        break
                    case _:
                        print('Wrong module number, try again')
                        continue
        except Exception as e:
            self.local_logger.log(f'Run console app failed - {e}')
            raise Exception()

    @log
    def run_app_browser(self):
        """
        Run application in browser
        :return: None
        """
        self.init_app_entities()
        try:
            self.local_logger.log(f'Web process run on pid {os.getpid()}')
            webinterface = Web_interface(logger=self.local_logger)
            webinterface.run_interface()
        except Exception as e:
            self.local_logger.log(f'Run browser app failed - {e}')
            raise Exception()

    @log
    def help_distribution_manager(self):
        print(f'{APP_NAME} utility')
        print('Description:')
        print('You can manage your saved books with help of this utility.')
        print('')
        print('')
        print('')
        print('')

#################################################################################
