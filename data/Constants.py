from typing import Final

from core.entities.BotLogger import BotLogger

BOOK_EXTENSIONS: Final[list[str]] = ['lrf', 'rar', 'zip', 'rtf', 'lit', 'txt', 'txtz', 'text', 'htm', 'xhtm',
                                     'html', 'htmlz', 'xhtml', 'pdf', 'pdb', 'updb', 'pdr', 'prc', 'mobi',
                                     'azw', 'doc',
                                     'epub', 'fb2', 'fbz', 'djv', 'djvu', 'lrx', 'cbr', 'cb7', 'cbz', 'cbc',
                                     'oebzip',
                                     'rb', 'imp', 'odt', 'chm', 'tpz', 'azw1', 'pml', 'pmlz', 'mbp', 'tan',
                                     'snb',
                                     'xps', 'oxps', 'azw4', 'book', 'zbf', 'pobi', 'docx', 'docm', 'md',
                                     'textile', 'markdown', 'ibook', 'ibooks', 'iba', 'azw3', 'ps', 'kepub',
                                     'kfx', 'kpf']

"""
Extensions of the books to be located by listing all files in directory.
"""

NON_BOOK_EXTENSIONS: Final[list[str]] = [
    'jpg', 'jpeg', 'gif', 'png', 'bmp',
    'opf', 'swp', 'swo'
]
"""
Other file extensions, not books extensions
"""

INPUT_SYM: Final[str] = '>> '

CLOSE_MENU_CODE: Final[str] = '666'
"""
Code for close menu functionality
"""

STATIC_FILE_NAME_WITH_READ: Final[str] = 'read.txt'
"""
Static file name of the read file.
"""

AUTHOR: Final[str] = 'KIRILL'
"""
Also known as Bob-jacka (Cupcake_wrld)
"""

APP_VERSION: Final[str] = '3.2.0'

global_logger: Final[BotLogger] = BotLogger()
"""
Global instance of logger class.
Change logger parameter to turn on logs in console.
Logger creates in different branches of app execution.
"""
