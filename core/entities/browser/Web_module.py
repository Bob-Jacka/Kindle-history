import os

PYTHON_INTERPRETER = 'python'
FILE_TO_ACTIVATE = '/home/kirill/PycharmProjects/KindleHistory/core/entities/browser/WebInterface/manage.py'
COMMAND = 'runserver'


class Web_interface:
    """
    Class responsible for web interface of the utility
    """

    def __init__(self, logger):
        self.logger = logger

    def run_interface(self):
        """
        Entry point
        Open browser and create all components in it
        :return: None
        """
        # TODO delete hardcoded command
        self.logger.log('Server starting work')
        self.__start_server()
        self.logger.log('Server ending work')

    def __start_server(self):
        os.system(f"{PYTHON_INTERPRETER} {FILE_TO_ACTIVATE} {COMMAND}")
        os.system(f"{PYTHON_INTERPRETER} {FILE_TO_ACTIVATE} {COMMAND} 8080")
        os.system(f"{PYTHON_INTERPRETER} {FILE_TO_ACTIVATE} {COMMAND} 0.0.0.0:8000")
        os.system(f"{PYTHON_INTERPRETER} {FILE_TO_ACTIVATE} {COMMAND} 192.168.1.100:8000")
        os.system(f"{PYTHON_INTERPRETER} {FILE_TO_ACTIVATE} {COMMAND} --noreload")
