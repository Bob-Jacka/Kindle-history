import os
from pathlib import Path
from typing import Final

from core.entities.BotLogger import BotLogger
from core.entities.Formatter import Format
from data.Constants import INPUT_SYM

_config_name: str = 'config.txt'


class App_config:
    """
    Class for configuration application with parameters.
    Simple store variables app configuration.
    Also store and manage paths in utility.
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

    def __init__(self, read_book_file_name: str = '', is_auto: bool = False, is_logs: bool = False,
                 exclude_dirs: list = None):
        self.__read_book_file = read_book_file_name
        self.__is_auto_mode = is_auto
        self.__is_enable_logs = is_logs
        self.__exclude_directories = exclude_dirs
        self.__central_dir = os.getcwd()  # get current directory
        self.__current_dir = self.__central_dir

    @staticmethod
    def get_help_config(self) -> None:
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
        if not os.path.exists(_config_name):
            print('Config is not exits')
            while True:
                print('Would you like to create test config file in this directory - yes (y) or no (n)?')
                user_input = input(INPUT_SYM)
                if user_input == 'yes' or user_input == 'y':
                    App_config.create_tmp_config()
                    break
                else:
                    break

    def path_to_read_file(self):
        return self.__central_dir + self.__read_book_file

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
                    elif line.startswith('central_dir'):
                        self.__central_dir = split_line[1]
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
            with open(_config_name, 'w+') as tmp_config:
                tmp_config.write('read_book_file_name: read.txt')
                tmp_config.write('\n')
                tmp_config.write('is_auto_mode: false')
                tmp_config.write('\n')

                tmp_config.write('is_enable_logs: false')
                tmp_config.write('\n')
                tmp_config.write('exclude_directories: None')
                tmp_config.write('\n')
                tmp_config.write('central_dir: None')
                tmp_config.write('\n')
            print('Config file created successfully')
        except Exception as e:
            print(f'Exception in create config file - {e}')
