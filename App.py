import os
import sys
from multiprocessing import Process

from core.entities.App_config import App_config
from core.entities.BootLoader import BootLoader
from core.entities.BotLogger import BotLogger
from core.entities.Translator import Translator
from data.Constants import (
    APP_NAME,
    STATIC_READ_FILE_NAME,
    STATIC_CONFIG_NAME
)

__global_logger: BotLogger = None
__translator: Translator = None

__app_config: App_config


class LW_process:
    """
    Process lightweight abstraction
    """
    __process_name: str
    __pid: int
    __process: Process

    def __init__(self, name: str, target):
        self.__process_name = name
        self.__process = Process(target=target)
        self.__pid = self.__process.pid

    def get_pid(self):
        return self.__pid

    def get_process_name(self):
        return self.__process_name

    def still_alive(self):
        return self.__process.is_alive()

    def close_process(self):
        """
        End process
        :return: None
        """
        print(f'Process with name {self.__process_name} is finished')
        self.__process.close()

    def start_proc(self):
        print(f'{self.__process_name} started')
        self.__process.start()

    def swap_proc(self, process):
        """
        Replace process with another
        :param process: process to replace with
        :return: None
        """
        self.__process = process


__console_process: LW_process = None
__browser_process: LW_process = None


def __init_app() -> None:
    """
    Initialize some useful application variables.
    Contains in base class for strategies
    :return: None
    """
    global __global_logger, __app_config
    try:
        current_dir = App_config.path_to_dir_with_app()
        print('Check for config file in files directory by default name')
        os_name = sys.platform

        config_path = current_dir + STATIC_CONFIG_NAME  # path to look for config
        if not os.path.exists(config_path):
            __app_config = App_config(os_name)
            __global_logger.log('Config file not found, using default values in configuration')
        else:
            __app_config = App_config(os_name)
            __app_config.init_config(current_dir + STATIC_CONFIG_NAME)

        __global_logger.log(f'App initialized in "{current_dir}" path in filesystem')
        __global_logger.log('Checking for file with read file by default name')
        if os.path.exists(current_dir + STATIC_READ_FILE_NAME):
            __global_logger.log('Read books file found')
        else:
            __global_logger.log('Read books file not found')
        __global_logger.log('App initialized in manual mode')
        if __app_config.get_current_dir_name() is None:
            __global_logger.log('Current directory cannot be None.')
            raise Exception('Current directory cannot be None, init failed')
    except Exception as e:
        __global_logger.log(f'Some exception occurred in init app - {e}')
        raise Exception('Init app failed')


def __init_app_entities():
    global __global_logger
    try:
        __global_logger = BotLogger()
        __translator = Translator()
    except Exception as e:
        print(f'Error in initializing app entities - {e}')
        raise Exception(f'App initialization failed due to {e}')


def __start_app():
    is_multi: bool = __app_config.is_multithreaded_app_mode()

    global __console_process, __browser_process
    # Upper level error handling
    try:
        bootloader = BootLoader(logger=__global_logger, app_config=__app_config)
        # if false - run browser version without different process
        if is_multi:
            __browser_process = LW_process('browser', target=bootloader.run_app_browser)
            __browser_process.start_proc()
        else:
            bootloader.run_app_browser()

    except Exception as e:
        __global_logger.log(f'An exception occurred during app initialization - {e}')
        raise Exception(f'Start app functionality failed due to - {e}')


def __clean_app_entities():
    """
    Delete app entities in case of error or finish
    :return: None
    """
    global __global_logger, __translator, __console_process, __browser_process
    if __console_process is not None or __browser_process is not None:
        if __console_process.still_alive():
            __console_process.close_process()

        if __browser_process.still_alive():
            __browser_process.close_process()
        __global_logger = None
        __translator = None


if __name__ == '__main__':
    try:
        print(f'"{APP_NAME}" utility starting')
        __init_app_entities()
        __init_app()
        __start_app()
    except Exception as e:
        print(f'All functionality failed with exception - {e}, app exiting')
        __clean_app_entities()
    print(f'"{APP_NAME}" utility ending work, bye')
    exit(1)
