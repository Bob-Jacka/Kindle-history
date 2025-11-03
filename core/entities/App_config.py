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
