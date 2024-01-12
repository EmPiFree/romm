import os
import re
from abc import ABC

from config import LIBRARY_BASE_PATH
from config.config_loader import config
from handler.fs_handler import EXTENSION_REGEX, TAG_REGEX


class FSHandler(ABC):
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_fs_structure(fs_slug: str, folder: str = config.ROMS_FOLDER_NAME):
        return (
            f"{folder}/{fs_slug}"
            if os.path.exists(config.HIGH_PRIO_STRUCTURE_PATH)
            else f"{fs_slug}/{folder}"
        )

    @staticmethod
    def _get_file_name_with_no_extension(file_name: str) -> str:
        return re.sub(EXTENSION_REGEX, "", file_name).strip()

    @staticmethod
    def get_file_name_with_no_tags(file_name: str) -> str:
        file_name_no_extension = re.sub(EXTENSION_REGEX, "", file_name).strip()
        return re.split(TAG_REGEX, file_name_no_extension)[0].strip()

    @staticmethod
    def parse_file_extension(file_name) -> str:
        match = re.search(EXTENSION_REGEX, file_name)
        return match.group(1) if match else ""

    def build_upload_file_path(
        self, fs_slug: str, folder: str = config.ROMS_FOLDER_NAME
    ):
        rom_path = self.get_fs_structure(fs_slug, folder=folder)
        return f"{LIBRARY_BASE_PATH}/{rom_path}"
