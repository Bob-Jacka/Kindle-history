"""
Module that responsible for interaction with file system on your pc
"""
import csv
import os
import re
import shutil
import stat
from os import PathLike
from sys import platform

from core.entities.Formatter import Format
from core.other.Utils import (
    print_success,
    print_error,
    user_input_cursor
)


class File_controller_tests:
    pass


class Csv_helper:
    pass


class Json_helper:
    pass


class Yaml_helper:
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

    def delete_fs_entity(self, path: str | os.PathLike) -> None:
        """
        Function for deleting book in given path, also can delete directory with save points;
        :param path: path to book
        :return: None
        """
        global_logger.log('Delete fs entity invoked')
        if path is not None:

            # file branch
            if os.path.isfile(path):
                try:
                    if path.endswith(self.path_to_read_file):
                        global_logger.log('You cannot delete your read file!')
                    else:
                        os.remove(path)
                        Format.prGreen('Book deleted from directory')
                except Exception as e:
                    global_logger.log(f'Exception occurred in deleting book in {path} - {e}')

            # directory branch
            elif os.path.isdir(path):
                try:
                    shutil.rmtree(path)
                    Format.prGreen(f'Directory {path} deleted')
                except Exception as e:
                    global_logger.log(f'Exception occurred in deleting directory in {path} - {e}')
        else:
            global_logger.log('Path cannot be None')

    def copy_fs_entity(self, path: str | os.PathLike, dir_name: str = '') -> None:
        """
        Save your book in central directory (app installation home).
        :param path: path from where you want to copy read book.
        :param dir_name: *optional parameter, special for directory copying. Use for creating new directory and copy all into
        :return: None
        """
        # global_logger.log('Copy fs entity invoked')
        if path is not None:

            # file branch
            if os.path.isfile(path):
                try:
                    shutil.copy2(path, central_dir)  # {src} {dest}
                    Format.prGreen('Book save in central directory')
                except Exception as e:
            # global_logger.log(f'Error occurred while saving book in central dir - {e}')

            # directory branch
            elif os.path.isdir(path):
                try:
                    new_save_point_path = central_dir + os.sep + dir_name
                    os.mkdir(new_save_point_path)  # create new directory, instead of deleting old
                    shutil.copytree(path, new_save_point_path, dirs_exist_ok=True)  # {src} {dest}
                    Format.prGreen('Directory save in central directory')
                except Exception as e:
            # global_logger.log(f'Error occurred while saving directory in central dir - {e}')

            else:
                Format.prRed('Object type nor file or directory')
                raise Exception(f'Cannot determine object type of {path}')
            self.delete_fs_entity(path)
        else:

    # global_logger.log('Path cannot be None')

    def creation_date(self, path_to_file: str | os.PathLike) -> str:
        """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
        """
        if platform.system() == Fs_utility.OSType.windows_os:
            return str(os.path.getctime(path_to_file))
        elif platform.system() == Fs_utility.OSType.linux_os:
            try:
                mtime = os.path.getmtime(path_to_file)
                mtime_readable = datetime.date.fromtimestamp(mtime)
                return str(mtime_readable)
            except AttributeError:
                return str(datetime.datetime.now())
        else:
            raise NotImplemented('It seems that you have Mac operating system, not implemented for this system')

    def is_book(self, name: str) -> bool:
        """
        Function for filtering directory for books
        :param name: name of the file to proceed
        :return: bool value, if name ended with 'book' extensions.
        """
        ext = os.path.splitext(name)[1]
        if not ext:
            return False
        ext = ext[1:].lower()
        bad_ext_pat = re.compile(r'[^a-z0-9_]+')
        if ext in self.non_ebook_extensions or bad_ext_pat.search(ext) is not None:
            return False
        return True
