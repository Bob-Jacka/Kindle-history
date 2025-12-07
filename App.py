import os
from multiprocessing import Process

from core.entities.BootLoader import BootLoader
from core.entities.BotLogger import BotLogger
from core.entities.Formatter import Format
from core.entities.Translator import Translator
from core.entities.console.App_config import App_config
from data.Constants import (
    APP_NAME,
    INPUT_SYM,
    STATIC_READ_FILE_NAME,
    STATIC_CONFIG_NAME
)

__global_logger: BotLogger = None
__translator: Translator = None

__app_config: App_config

__console_process: Process = None
__browser_process: Process = None


def __init_app() -> None:
    """
    Initialize some useful application variables.
    Contains in base class for strategies
    :return: None
    """
    global __global_logger, __app_config
    try:
        current_dir = App_config.get_real_path()
        print('Check for config file in files directory by default name')
        if not os.path.exists(App_config.get_real_path(STATIC_CONFIG_NAME)):
            __app_config = App_config()
            __global_logger.log('Config file not found, using default values in configuration')
        else:
            __app_config = App_config()
            __app_config.init_config(current_dir + STATIC_CONFIG_NAME)

        __global_logger.log(f'App initialized in "{current_dir}" path in filesystem')
        __global_logger.log('Checking for file with read file by default name')
        if os.path.exists(current_dir + STATIC_READ_FILE_NAME):
            __global_logger.log('Read books file found')
        else:
            __global_logger.log('Read books file not found')
            Format.prYellow('Would you like to create file with read books? (yes(y) /no (n))')
            user_choice = input(INPUT_SYM)
            if user_choice == 'yes' or user_choice == 'y':
                os.mknod(__app_config.get_central_dir_name() + os.sep + STATIC_READ_FILE_NAME)
                __global_logger.log('File for your book history created!')
            else:
                __global_logger.log('Read file not found or create')
                raise Exception('Read file not found, init failed')
        __global_logger.log('App initialized in manual mode')
        if __app_config.get_current_dir_name() is None:
            __global_logger.log('Current directory cannot be None.')
            raise Exception('Current directory cannot be None, init failed')
    except Exception as e:
        __global_logger.log(f'Some exception occurred in init app - {e}')
        raise Exception('Init app failed')


def __init_app_entities():
    global __global_logger, __translator
    try:
        __global_logger = BotLogger()
        __translator = Translator()
    except Exception as e:
        print(f'Error in initializing app entities - {e}')
        raise Exception('App initialization failed')


def __start_app():
    mode: bool = __app_config.get_app_mode()

    global __console_process, __browser_process
    # Upper level error handling
    try:
        bootloader = BootLoader(logger=__global_logger, app_config=__app_config)
        if mode:
            __console_process = Process(target=bootloader.run_app_console)
            __console_process.start()
        else:
            __browser_process = Process(target=bootloader.run_app_browser)
            __browser_process.start()

    except Exception as e:
        __global_logger.log(f'An exception occurred during initialization - {e}')
        raise Exception('Start app functionality failed')


def __clean_app_entities():
    global __global_logger, __translator, __console_process, __browser_process
    if __console_process is not None or __browser_process is not None:
        if __console_process.is_alive() or __browser_process.is_alive():
            __console_process.close()
            __global_logger.log('Console process closed')
            __browser_process.close()
            __global_logger.log('Browser process closed')
        __global_logger = None
        __translator = None


if __name__ == '__main__':
    try:
        print(f'"{APP_NAME}" utility starting')
        __init_app()
        __init_app_entities()
        __start_app()
    except Exception as e:
        print('All functionality failed, app exiting')
        __clean_app_entities()
    print(f'"{APP_NAME}" utility ending work, bye')
    exit(1)
