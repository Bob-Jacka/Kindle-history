import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

from core.entities.BotLogger import BotLogger
from core.entities.Formatter import Format
from data.Constants import INPUT_SYM


class Config_param_names(Enum):
    """
    Enum class with config names to proceed
    """
    READ_BOOK_FILE_NAME = 'read_book_file'
    AUTO_MODE = 'is_auto_mode'
    ENABLE_LOGS = 'is_enable_logs'
    EXCLUDE_DIRS = 'exclude_directories'
    CENTRAL_DIR = 'central_dir'
    APP_MODE = 'app_mode'


@dataclass
class App_config:
    """
    Class for configuration application with parameters.
    Simple store variables app configuration.
    Also store and manage paths in utility.
    """

    __read_book_file: str
    """
    Default name of the file with read book.
    """

    __config_name: str
    """
    Default name of the config file
    """

    __is_auto_mode: bool
    """
    Is auto resolve books and auto mode in Kindle history module.
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

    __central_dir: str
    """
    directory address where app stored (home directory path)
    """

    __current_dir: str
    """
    pointer to current working directory of the application
    """

    __global_logger: Final[BotLogger] = BotLogger()
    """
    Global instance of logger class.
    Change logger parameter to turn on logs in console.
    Logger creates in different branches of app execution.
    """

    def __init__(self, read_book_file_name: str = 'read.txt', config_file_name: str = 'config.txt',
                 is_auto: bool = True, is_logs: bool = False, exclude_dirs: list = None):
        # Main config parameters:
        self.app_mode = None
        self.__central_dir = self.get_real_path()  # get current directory
        self.__current_dir = self.__central_dir

        # Other config parameters:
        self.__read_book_file = read_book_file_name
        self.__config_name = config_file_name
        self.__is_auto_mode = is_auto  # also used for interactive or not mode
        self.__is_enable_logs = is_logs  # turn off if you want to disable logs
        self.__exclude_directories = exclude_dirs

    def get_help_config(self) -> None:
        print('App config help.')
        print('Config can contain next parameters:')
        print('1. read_book_file_name - name of the file with read books,')
        print('2. is_auto_mode - turn on by default auto mode in application,')
        print('3. is_enable_logs - turn on of off logs in application,')
        print('4. exclude_directories - which directories to ignore by book search.')
        print('5. home directory - start directory of the app work.')
        print('How to write config file:')
        print('Write in config file next lines')

        print('read_book_file_name: <your file name>')
        print('is_auto_mode: <true or false values>')
        print('is_enable_logs: <true or false values>')
        print('exclude_directories: <one_dir_name, second_dir_name, third_dir_name> (list with dirs names)')
        if not os.path.exists(self.__config_name):
            print('Config is not exits')
            while True:
                print('Would you like to create test config file in this directory - yes (y) or no (n)?')
                user_input = input(INPUT_SYM)
                if user_input == 'yes' or user_input == 'y':
                    App_config.create_tmp_config()
                    break
                else:
                    break

    def path_to_read_file(self) -> str:
        return self.__central_dir + self.__read_book_file

    def init_config(self, config_file_name: str) -> None:
        """
        Initialize app by given config.
        Parse config file and get line by line parameters
        :param config_file_name: name of the config file to init.
        :return: None
        """
        with open(config_file_name) as file:
            for line in file:
                if ':' in line:
                    split_line = line.split(':')
                    value = split_line[1].strip()  # value for setting into configuration parameter
                    if value != '':
                        if line.startswith(Config_param_names.READ_BOOK_FILE_NAME.value):
                            self.__read_book_file = value
                        elif line.startswith(Config_param_names.ENABLE_LOGS.value):
                            self.__is_enable_logs = bool(value)
                        elif line.startswith(Config_param_names.AUTO_MODE.value):
                            self.__is_auto_mode = bool(value)
                        elif line.startswith(Config_param_names.EXCLUDE_DIRS.value):
                            self.__exclude_directories = list(value)
                        elif line.startswith(Config_param_names.CENTRAL_DIR.value):
                            self.__central_dir = value
                        elif line.startswith(Config_param_names.APP_MODE.value):
                            self.app_mode = value
                        else:
                            raise Exception(f'Wrong config parameter - {line}')
                    else:
                        print(f'Value cannot be none in {line}')
                else:
                    raise Exception(f'Wrong config parameter split symbol - {line}')
            else:
                raise Exception('Exception in checking lines')

    def get_read_file_name(self):
        if self.__read_book_file is not None:
            return self.__read_book_file
        else:
            raise Exception('Try to get null value')

    def get_config_file_name(self):
        if self.__config_name is not None:
            return self.__config_name
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

    def get_central_dir_name(self):
        if self.__central_dir is not None:
            return self.__central_dir
        else:
            raise Exception('File with read books is not initialized')

    def get_current_dir_name(self):
        if self.__current_dir is not None:
            return self.__current_dir
        else:
            raise Exception('File with read books is not initialized')

    def get_logger(self):
        return self.__global_logger

    def move_upper(self):
        """
        Move upper in file system tree
        :return: None
        """
        __current_dir = Path(self.__current_dir).parent

    def move_lower(self):
        """
        Move lower in file system tree
        :return: None
        """
        p = Path(
            '../../..')  # check current directory
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
            print(f'Or {777}: to exit this menu')

            while True:
                print('Enter dir number to move in')
                dir_number = int(input(777))
                if dir_number in range(len(dir_list)):
                    __current_dir = dir_list[dir_number].as_posix()
                    break
                elif dir_number == int(777):
                    self.__global_logger.log('Close menu')
                    break

    @staticmethod
    def create_tmp_config():
        """
        Creates config if you cannot do it by yourself.
        :return: None
        """
        try:
            with open('config.txt', 'w+') as tmp_config:
                tmp_config.write(f'{Config_param_names.READ_BOOK_FILE_NAME.value}: read.txt')
                tmp_config.write('\n')
                tmp_config.write(f'{Config_param_names.AUTO_MODE.value}: false')
                tmp_config.write('\n')

                tmp_config.write(f'{Config_param_names.ENABLE_LOGS.value}: false')
                tmp_config.write('\n')
                tmp_config.write(f'{Config_param_names.EXCLUDE_DIRS.value}: None')
                tmp_config.write('\n')
                tmp_config.write(f'{Config_param_names.CENTRAL_DIR.value}: None')
                tmp_config.write('\n')
            print('Config file created successfully with default parameters in it')
        except Exception as e:
            print(f'Exception in create config file - {e}, file not created')

    @staticmethod
    def get_real_path(end_with: str = '') -> str:
        """
        Get real path to file with back system separator if you not provide end_with value.
        By default, return path to central directory (utility home)
        :param end_with: value that will be inserted at back of the path
        :return: string value, representing path in your system
        """
        return Path(os.getcwd()).parent.absolute().as_posix() + os.sep + end_with

    def get_app_mode(self):
        return self.app_mode
