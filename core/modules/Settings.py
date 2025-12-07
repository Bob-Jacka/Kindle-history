"""
Settings module
Not used outside of distribution manager, used only for in-app settings
"""

from core.entities.console.AbstractModule import Module
from core.other.Utils import int_input_from_user
from data.Wrappers import log


class Setting(Module):

    def __init__(self):
        """
        Settings module
        """
        self.config = None

    @log
    def post_init(self, app_config):
        self.config = app_config

    @log
    def __change_config(self):
        while True:
            print('Enter action number to change in config:')
            print('1. Change is auto mode variable')
            print('2. Change ')
            print('3. To close menu')
            user_choice = int_input_from_user(3)
            match user_choice:
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    break

    @log
    def __utility_settings(self):
        while True:
            print('Enter action number to change in utility:')
            print('')
            print('')
            print('3. To close menu')
            user_choice = int_input_from_user(3)
            match user_choice:
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    break

    def run_module(self) -> None:
        while True:
            print('Enter action number to :')
            print('1. Change config')
            print('2. Utility settings')
            print('3. Exit module')

            user_choice = int_input_from_user(values_range=3)
            match user_choice:
                case 1:
                    self.__change_config()
                case 2:
                    self.__utility_settings()
                case 3:
                    break
