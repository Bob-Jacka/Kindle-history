"""
Module that responsible for interaction with file system on your pc
"""
import csv
import os
import stat
from os import PathLike

from core.other.Utils import (
    print_success,
    print_error,
    user_input_cursor
)


class File_controller_tests:
    pass


class File_controller:

    def create_log_file(self, log_file_name: str):
        pass

    @staticmethod
    def __update_data_csv(labels_dir_path: str | PathLike, images_dir_name: str = 'images',
                          labels_file_name: str = 'labels.csv'):
        """
        Static function for updating labels in csv file.
        Opens file if it exits or creates new file if it not and then rewritten (written) data to file on every call.
        Before every call unlocks file for writing, after every call locks file for writing.
        RULES:
            1. Images names must ends with {success_img_indicator} or {failure_img_indicator}.
            2. labels_file_name must include '.csv' extension.
            3. labels_dir_path must fill out in main.py file.
        :param labels_dir_path path where labels are stored.
        :param images_dir_name path where images are stored.
        :param labels_file_name: name of the labels file.
        :return: None.
        """

    full_path = labels_dir_path + labels_file_name
    try:
        os.chmod(full_path, stat.S_IWUSR)
        with open(full_path, 'w+') as csvfile:
            csvwriter = csv.writer(csvfile, lineterminator='\n')
            row: list = list()  # row of the csv file.
            images_path_dir: str = labels_dir_path + images_dir_name
            csvwriter.writerow(['Games', 'Value'])  # writes down headers to csv file.
            for file_name in os.listdir(images_path_dir):
                if file_name.endswith(success_img_indicator):
                    label = test_labels['Success']  # 1 - value for success.
                    row.append(file_name)
                    row.append(label)
                elif file_name.endswith(failure_img_indicator):
                    label = test_labels['Failed']  # 0 - value for failure.
                    row.append(file_name)
                    row.append(label)
                else:
                    print_error(
                        f'Unknown image identifier. Expected image ending with - {success_img_indicator} or {failure_img_indicator}.')
                csvwriter.writerow(row)
                row = list()
        print_success('Labels have been updated.')
        print_success('Exit program to update file view.')
        csvfile.close()
        os.chmod(full_path, stat.SF_IMMUTABLE)
    except Exception as e:
        print_error(f'Error in update labels because - {e.with_traceback(None)}.')
        os.chmod(full_path, stat.SF_IMMUTABLE)

    def __update_data_json(self):
        pass

    def __update_data_yaml(self):
        pass

    def write_to_storage(self, record):
        """
        Entry point to file controller class to write data to storage.
        :param record: Record class in database
        :return: None
        """
        pass

    def do_backup_copy(self) -> None:
        """
        Function for backup your books in given directory (Download dir).
        :return: None
        """
        global_logger.log('Backup books invoked')
        save_path: str | os.PathLike
        if platform.system() == Fs_utility.OSType.windows_os:
            save_path = Path.home().as_uri() + os.sep + 'Downloads'
            global_logger.log('Windows user path to Downloads')
        elif platform.system() == Fs_utility.OSType.linux_os:
            save_path = Path.home().as_uri() + os.sep + 'Downloads'
            global_logger.log('Linux user path to Downloads')
        else:
            raise Exception('Unknown operating system, not implemented yet.')

        for dir in os.listdir(central_dir):
            self.copy_fs_entity(dir, save_path)
            global_logger.log(f'File - {dir} backed up in {save_path}')

    def reset_data(self) -> None:
        """
        Method for deleting all book data (exclude file with book read).
        Also home directory of the app will be saved.
        :return: None
        """
        while True:
            print('Do you really want to delete all books data? yes (y) or no (n)')
            user_choice = input(user_input_cursor)
            if user_choice == 'yes' or user_choice == 'y':
                global_logger.log('Reset data is invoked')
                dir_list = self.get_book_data_dirs_list()
                for dir in dir_list:
                    self.delete_fs_entity(dir)
            elif user_choice == 'no' or user_choice == 'n':
                global_logger.log('Reset data canceled')
            else:
                print('Wrong choice, try again')
                continue
