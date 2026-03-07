"""
Calibre connector module for interacting with Calibre library via Python API.
"""

import os
from pathlib import Path
from typing import Optional

from core.entities.console.AbstractModule import Module
from core.exceptions.TransferBookException import TransferBookException
from data.Wrappers import log

from calibre.devices.scanner import DeviceScanner
from calibre.devices import devices


class USB_calibre(Module):
    """
    USB device connector for e-book readers using Calibre device drivers.
    Supports Kindle, Kobo, PocketBook and other devices.
    """

    def __init__(self):
        self._scanner: Optional[DeviceScanner] = None
        self._connected_device = None
        self._device_driver = None
        self.local_logger = None

    @log
    def post_init(self, app_config):
        """
        Initialize with app config.
        :param app_config: Application configuration object
        """
        self.config = app_config
        self.local_logger = app_config.get_logger()
        self._scanner = DeviceScanner()

    @log
    def detect_device(self) -> Optional[dict]:
        """
        Detect connected USB e-book device.
        :return: Device info dict or None if no device found
        """
        if self._scanner is None:
            self._scanner = DeviceScanner()

        self._scanner.scan()
        detected = self._scanner.detected_devices

        if not detected:
            return None

        # Find matching driver for detected device
        for dev_class in devices():
            try:
                if dev_class.is_device_present(detected[0]):
                    return {
                        'vendor': detected[0].vendor_id,
                        'product': detected[0].product_id,
                        'bus': detected[0].bus,
                        'device_class': dev_class.__name__,
                        'name': getattr(dev_class, 'name', 'Unknown'),
                        'driver': dev_class
                    }
            except Exception:
                continue

        return None

    @log
    def connect(self) -> None:
        """
        Connect to detected USB device.
        :raises TransferBookException: If no device found or connection failed
        """
        device_info = self.detect_device()

        if device_info is None:
            raise TransferBookException('No USB e-book device detected')  # or it can be an wrong

        try:
            self._device_driver = device_info['driver']
            self._connected_device = self._device_driver()
            self._connected_device.open()
            self.local_logger.log(f'Connected to device: {device_info["name"]}')
        except Exception as e:
            raise TransferBookException(f'Failed to connect to device: {e}')

    @log
    def get_device_info(self) -> dict:
        """
        Get information about connected device.
        :return: Device information dictionary
        """
        if self._connected_device is None:
            raise TransferBookException('No device connected')

        try:
            info = {
                'name': self._connected_device.get_device_name(),
                'manufacturer': getattr(self._connected_device, 'manufacturer', 'Unknown'),
                'model': getattr(self._connected_device, 'device_model', 'Unknown'),
                'total_space': self._connected_device.total_space(),
                'free_space': self._connected_device.free_space(),
            }
            return info
        except Exception as e:
            raise TransferBookException(f'Failed to get device info: {e}')

    @log
    def get_books_on_device(self) -> list[dict]:
        """
        Get list of books currently on device.
        :return: List of book dictionaries
        """
        if self._connected_device is None:
            raise TransferBookException('No device connected')

        try:
            books = self._connected_device.books()
            result = []
            for book in books:
                result.append({
                    'title': book.title,
                    'author': ', '.join(book.authors) if book.authors else 'Unknown',
                    'path': book.path,
                    'size': book.size,
                    'format': book.format
                })
            return result
        except Exception as e:
            raise TransferBookException(f'Failed to get books from device: {e}')

    @log
    def send_books(self, book_paths: list[str], metadata: list[dict] = None) -> None:
        """
        Send books to connected device.
        :param book_paths: List of paths to book files
        :param metadata: Optional list of metadata dicts for each book
        """
        if self._connected_device is None:
            raise TransferBookException('No device connected')

        if not book_paths:
            raise TransferBookException('No book paths provided')

        for path in book_paths:
            if not os.path.exists(path):
                raise TransferBookException(f'Book file not found: {path}')

        try:
            # Create book info objects for upload
            from calibre.ebooks.metadata.book.base import Metadata

            book_infos = []
            for i, path in enumerate(book_paths):
                meta = metadata[i] if metadata and i < len(metadata) else {}
                mi = Metadata(
                    title=meta.get('title', Path(path).stem),
                    authors=meta.get('authors', ['Unknown'])
                )
                book_infos.append((path, mi))

            self._connected_device.upload_books(book_infos, '/documents/')
            self.local_logger.log(f'Sent {len(book_paths)} books to device')
        except Exception as e:
            raise TransferBookException(f'Failed to send books to device: {e}')

    @log
    def delete_book(self, book_path: str) -> None:
        """
        Delete book from device.
        :param book_path: Path of book on device
        """
        if self._connected_device is None:
            raise TransferBookException('No device connected')

        try:
            self._connected_device.remove_book_from_device(book_path)
            self.local_logger.log(f'Deleted book: {book_path}')
        except Exception as e:
            raise TransferBookException(f'Failed to delete book: {e}')

    @log
    def disconnect(self) -> None:
        """
        Disconnect from current device.
        """
        if self._connected_device is not None:
            try:
                self._connected_device.close()
                self.local_logger.log('Disconnected from device')
            except Exception:
                pass
            finally:
                self._connected_device = None
                self._device_driver = None

    def is_connected(self) -> bool:
        """
        Check if device is currently connected.
        :return: True if connected
        """
        return self._connected_device is not None

    @log
    def run_module(self) -> None:
        """
        Entry point to module execution.
        """
        while True:
            print('Enter action number:')
            print('1. Connect to library')
            print('2. List books')
            print('3. Add book')
            print('4. Send to device')
            print('5. Disconnect')
            print('6. Exit')

            try:
                action = int(input('>> '))
                match action:
                    case 1:
                        path = input('Enter library path: ')
                        self.connect_to_library(path)
                    case 2:
                        books = self.get_books()
                        for book in books:
                            print(f"{book['id']}: {book['title']} - {book['author']}")
                    case 3:
                        file_path = input('Enter book file path: ')
                        self.add_book(file_path)
                    case 4:
                        device = input('Enter device mount path: ')
                        ids = input('Enter book IDs (comma separated): ')
                        book_ids = [int(x.strip()) for x in ids.split(',')]
                        self.send_to_device(book_ids, device)
                    case 5:
                        self.disconnect()
                    case 6:
                        print('Bye')
                        break
            except ValueError:
                print('Invalid input')
                continue
            except TransferBookException as e:
                print(f'Error: {e.message}')


class Calibre_сonnector(Module):
    """
    Connector for Calibre e-book manager using Python API.
    Provides methods to manage library, books and device connection.
    """

    def __init__(self):
        self.local_logger = None
        self.config = None
        self._library_path: Optional[str] = None
        self._db = None  # calibre.library.db.ReadonlyTree

    @log
    def post_init(self, app_config):
        """
        Post construct method for initializing config file in module.
        :param app_config: Application configuration object
        :return: None
        """
        self.config = app_config
        self.local_logger = app_config.get_logger()

    @log
    def connect_to_library(self, library_path: str) -> None:
        """
        Connect to Calibre library at specified path.
        :param library_path: Path to Calibre library folder
        :raises TransferBookException: If library not found or invalid
        """
        if not os.path.exists(library_path):
            raise TransferBookException(f'Library path does not exist: {library_path}')

        metadata_db = os.path.join(library_path, 'metadata.db')
        if not os.path.exists(metadata_db):
            raise TransferBookException(f'Not a valid Calibre library: {library_path}')

        try:
            from calibre.library import db
            self._db = db(library_path)
            self._library_path = library_path
            self.local_logger.log(f'Connected to Calibre library: {library_path}')
        except ImportError:
            raise TransferBookException(
                'Calibre Python API not found. Ensure Calibre is installed '
                'and calibre module is in PYTHONPATH'
            )

    @log
    def get_books(self) -> list[dict]:
        """
        Get list of all books in connected library.
        :return: List of book dictionaries with metadata
        """
        if self._db is None:
            raise TransferBookException('Not connected to any library')

        books = []
        for book_id in self._db.all_book_ids():
            book_data = self._db.get_metadata(book_id)
            books.append({
                'id': book_id,
                'title': book_data.title,
                'author': ', '.join(book_data.authors),
                'formats': self._db.formats(book_id),
                'tags': list(book_data.tags)
            })
        return books

    @log
    def add_book(self, file_path: str, add_duplicates: bool = False) -> int:
        """
        Add book to Calibre library.
        :param file_path: Path to book file
        :param add_duplicates: Allow adding duplicate books
        :return: Book ID of added book
        """
        if self._db is None:
            raise TransferBookException('Not connected to any library')

        if not os.path.exists(file_path):
            raise TransferBookException(f'Book file not found: {file_path}')

        try:
            book_id, duplicates = self._db.add_book(
                [file_path],
                add_duplicates=add_duplicates
            )
            if duplicates:
                self.local_logger.log(f'Book added with duplicates: {file_path}')
            return book_id
        except Exception as e:
            raise TransferBookException(f'Failed to add book: {e}')

    @log
    def get_book_formats(self, book_id: int) -> list[str]:
        """
        Get available formats for a book.
        :param book_id: Book identifier
        :return: List of available formats (e.g., ['EPUB', 'PDF'])
        """
        if self._db is None:
            raise TransferBookException('Not connected to any library')

        return self._db.formats(book_id) or []

    @log
    def get_book_path(self, book_id: int, fmt: str) -> Optional[str]:
        """
        Get file path for book in specified format.
        :param book_id: Book identifier
        :param fmt: Format (e.g., 'EPUB', 'PDF')
        :return: Path to book file or None
        """
        if self._db is None:
            raise TransferBookException('Not connected to any library')

        return self._db.format_abspath(book_id, fmt.upper())

    @log
    def send_to_device(self, book_ids: list[int], device_path: str) -> None:
        """
        Send books to connected e-book device.
        :param book_ids: List of book IDs to send
        :param device_path: Path where device is mounted
        """
        if self._db is None:
            raise TransferBookException('Not connected to any library')

        if not os.path.ismount(device_path):
            raise TransferBookException(f'Device not mounted at: {device_path}')

        for book_id in book_ids:
            formats = self._db.formats(book_id)
            if not formats:
                raise TransferBookException(f'No formats available for book ID {book_id}')

            # Prefer EPUB, then MOBI, then first available
            preferred = next((f for f in formats if f.upper() in ['EPUB', 'MOBI']), formats[0])
            book_path = self._db.format_abspath(book_id, preferred)

            if book_path:
                dest_path = os.path.join(device_path, 'documents', os.path.basename(book_path))
                self._copy_to_device(book_path, dest_path)

    def _copy_to_device(self, src: str, dest: str) -> None:
        """
        Internal method to copy file to device.
        :param src: Source file path
        :param dest: Destination file path
        """
        import shutil
        try:
            shutil.copy2(src, dest)
            self.local_logger.log(f'Copied: {src} -> {dest}')
        except Exception as e:
            raise TransferBookException(f'Failed to copy to device: {e}')

    @log
    def disconnect(self) -> None:
        """
        Disconnect from current library.
        """
        if self._db is not None:
            self._db.close()
            self._db = None
            self._library_path = None
            self.local_logger.log('Disconnected from Calibre library')

    @log
    def run_module(self) -> None:
        """
        Entry point to usb module execution.
        """
        while True:
            print('Enter action number:')
            print('1. Connect to library')
            print('2. List books')
            print('3. Add book')
            print('4. Send to device')
            print('5. Disconnect')
            print('6. Exit')

            try:
                action = int(input('>> '))
                match action:
                    case 1:
                        path = input('Enter library path: ')
                        self.connect_to_library(path)
                    case 2:
                        books = self.get_books()
                        for book in books:
                            print(f"{book['id']}: {book['title']} - {book['author']}")
                    case 3:
                        file_path = input('Enter book file path: ')
                        self.add_book(file_path)
                    case 4:
                        device = input('Enter device mount path: ')
                        ids = input('Enter book IDs (comma separated): ')
                        book_ids = [int(x.strip()) for x in ids.split(',')]
                        self.send_to_device(book_ids, device)
                    case 5:
                        self.disconnect()
                    case 6:
                        print('Bye')
                        break
            except ValueError:
                print('Invalid input')
                continue
            except TransferBookException as e:
                print(f'Error: {e.message}')
