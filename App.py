from core.entities.BootLoader import BootLoader
from core.entities.BotLogger import BotLogger
from core.entities.Translator import Translator
from data.Constants import APP_NAME

__global_logger = BotLogger()
__translator = Translator()

app_entities: tuple = tuple((__global_logger, __translator))

if __name__ == '__main__':
    mode: bool = False  # TODO.txt get from console or anywhere
    bootloader = BootLoader()
    print(f'"{APP_NAME}" utility starting')
    if mode:
        bootloader.run_app_console()
    else:
        bootloader.run_app_browser()
    print(f'"{APP_NAME}" utility ending work')
