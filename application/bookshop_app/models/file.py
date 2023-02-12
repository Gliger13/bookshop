"""File manager

Module contains an abstract file manager, various implementations of successors
and file manager factory. File manager is responsible for getting, saving and
deleting files from the remote. File manager factory produces different types
of file managers depends on the package configuration.
"""
import logging
import os
from abc import ABCMeta, abstractmethod
from enum import Enum
from functools import lru_cache
from typing import Mapping
from uuid import uuid4

from marshmallow import ValidationError
from PIL import Image
from werkzeug.datastructures import FileStorage

from bookshop_app.config import ConfigError, get_environment_config


class FileMangerType(Enum):
    """File manager type

    Enum contains all supported file manager types.
    """

    LOCAL = "local"


class BaseFileManager(metaclass=ABCMeta):
    """Abstract File Manager

    Provides basic file manager initialization interface and defines basic
    file operations such as getting, creating, deleting.
    """

    def __init__(self, file_manager_config: dict) -> None:
        """Initialize file manager using given file manager config

        :param file_manager_config: config for the current type of file manager
        """
        self._config = file_manager_config

    @abstractmethod
    def save(self, file_name: str, file_binary: bytes) -> str:
        """Save the given file binary with the given name in the remote

        :param file_name: name of the saved file to have
        :param file_binary: file binary data to save
        :return: path of the saved file in the remote
        """

    @abstractmethod
    def get(self, file_name: str) -> bytes | None:
        """Load file content from the remote with the given name

        :param file_name: name of the file to get from the remote
        :return: loaded file bytes or None if the file does not exist
        """

    @abstractmethod
    def delete(self, file_path: str) -> None:
        """Delete file with the given path in the remote

        :param file_path: file path in the remote to delete
        """


class LocalFileManager(BaseFileManager):
    """Local File Manager

    Implements a file manager for saving, getting, deleting files on the local
    filesystem.
    """

    def __init__(self, file_manager_config: dict):
        """Initialize Local File Manager with the given config

        Generate a directory path to save files based on the given config.
        Create a directory tree for the generated directory to save files if it
        has not already been created.

        :param file_manager_config: config for the local file manager
        """
        super().__init__(file_manager_config)
        self.directory_path_to_save = self._config.get("dir_to_save", os.path.join("instance", "files"))
        self._initialize_local_directory_to_save_files()

    def save(self, file_name: str, file_binary: bytes) -> str:
        """Save the given file binary on local filesystem

        Save given file binary with generated UUID name and format from the
        file name in the directory specified in the configuration.

        :param file_name: name of the file to save
        :param file_binary: file bytes to save
        :return: local filesystem path to the saved file
        """
        file_format = file_name.split(".")[-1] if "." in file_name else ""
        unique_file_name = f"{uuid4()}.{file_format}" if file_format else str(uuid4())
        file_path_to_save = os.path.join(self.directory_path_to_save, unique_file_name)
        with open(file_path_to_save, "bw") as file:
            file.write(file_binary)
        logging.info("The file has been saved to the path: `%s`", file_path_to_save)
        return file_path_to_save

    def get(self, file_path: str) -> bytes | None:
        """Get file bytes from the local filesystem with the given path

        :param file_path: local filesystem path to get file
        :return: loaded file bytes or None if the file was not found
        """
        logging.debug("Getting a file from the local filesystem by path `%s`", file_path)
        file_name_to_get = os.path.basename(file_path)
        expected_file_path_to_get = os.path.join(self.directory_path_to_save, file_name_to_get)
        if os.path.exists(expected_file_path_to_get):
            with open(file_path, "br") as file:
                return file.read()
        else:
            logging.warning("File manager received file path to get outside the configured folder. Aborting")
            return None

    def delete(self, file_path: str) -> None:
        """Delete file from the local filesystem with the given path

        :param file_path: local filesystem path to delete
        """
        logging.debug("Deleting a file from the local filesystem by path `%s`", file_path)
        file_name_to_delete = os.path.basename(file_path)
        expected_file_path_to_delete = os.path.join(self.directory_path_to_save, file_name_to_delete)
        if os.path.exists(expected_file_path_to_delete):
            os.remove(expected_file_path_to_delete)
            logging.info("Image `%s` was deleted by path", file_name_to_delete)
        else:
            logging.warning("File manager received file path to delete outside the configured folder. Aborting")

    def _initialize_local_directory_to_save_files(self) -> None:
        """Create local directory tree for folder to save files if needed"""
        if not os.path.exists(self.directory_path_to_save):
            os.makedirs(self.directory_path_to_save)


class FileManagerFactory:
    """File manager factory

    Factory that produces different file managers depending on the configuration.
    """

    FILE_MANAGER_TYPE_AND_MANAGER_MAP: Mapping[FileMangerType, type[BaseFileManager]] = {
        FileMangerType.LOCAL: LocalFileManager,
    }

    @classmethod
    @lru_cache
    def get_by_environment_config(cls) -> BaseFileManager:
        """Get file manager using current environment config

        :raise ConfigError: if the file manager type from config is not found
        :return: initialized file manager for the file manager type specified
            in the current environment config
        """
        file_manager_config = get_environment_config().FILE_MANAGER_CONFIG
        raw_file_manager_type = file_manager_config.pop("file_manager_type", None)
        if raw_file_manager_type in FileMangerType.__members__:
            file_manager_type = FileMangerType(raw_file_manager_type)
        else:
            raise ConfigError("File manager type specified in the current environment configuration was not found. "
                              f"Was specified: `{raw_file_manager_type}`")
        file_manager = cls.FILE_MANAGER_TYPE_AND_MANAGER_MAP.get(file_manager_type)(file_manager_config)
        return file_manager


class FileValidator:
    """Validator for all file related validations"""

    @staticmethod
    def validate_image(image: FileStorage) -> None:
        """Validate that given image from the requests is an image

        :param image: image from the request files to check
        """
        image_to_validate = Image.open(image)
        try:
            image_to_validate.verify()
        except Exception:
            raise ValidationError("Verification of uploaded image failed")
