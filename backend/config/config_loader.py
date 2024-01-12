import os
import sys
from typing import Final
from urllib.parse import quote_plus

import pydash
import yaml
from config import (DB_HOST, DB_NAME, DB_PASSWD, DB_PORT, DB_USER,
                    ROMM_BASE_PATH, ROMM_DB_DRIVER)
from logger.logger import log
from yaml.loader import SafeLoader

ROMM_USER_CONFIG_PATH: Final = f"{ROMM_BASE_PATH}/config.yml"
SQLITE_DB_BASE_PATH: Final = f"{ROMM_BASE_PATH}/database"


from config import LIBRARY_BASE_PATH


class Config:
    EXCLUDED_PLATFORMS: list[str]
    EXCLUDED_SINGLE_EXT: list[str]
    EXCLUDED_SINGLE_FILES: list[str]
    EXCLUDED_MULTI_FILES: list[str]
    EXCLUDED_MULTI_PARTS_EXT: list[str]
    EXCLUDED_MULTI_PARTS_FILES: list[str]
    PLATFORMS_BINDING: dict[str, str]
    ROMS_FOLDER_NAME: str
    SAVES_FOLDER_NAME: str
    STATES_FOLDER_NAME: str
    SCREENSHOTS_FOLDER_NAME: str
    HIGH_PRIO_STRUCTURE_PATH: str

    def __init__(self, **entries):
        self.__dict__.update(entries)
        self.HIGH_PRIO_STRUCTURE_PATH = f"{LIBRARY_BASE_PATH}/{self.ROMS_FOLDER_NAME}"


class ConfigLoader:
    """Parse and load the user configuration from the config.yml file

    Raises:
        FileNotFoundError: Raises an error if the config.yml is not found
    """

    # Tests require custom config path
    def __init__(self, config_path: str = ROMM_USER_CONFIG_PATH):
        self.config_path = config_path
        if os.path.isdir(config_path):
            log.critical(
                f"Your config file {config_path} is a directory, not a file. Docker creates folders by default for binded files that doesn't exists in advance in the host system."
            )
            raise FileNotFoundError()
        try:
            with open(config_path) as config_file:
                self._raw_config = yaml.load(config_file, Loader=SafeLoader) or {}
        except FileNotFoundError:
            self._raw_config = {}
        finally:
            self._parse_config()

    @staticmethod
    def get_db_engine() -> str:
        """Builds the database connection string depending on the defined database in the config.yml file

        Returns:
            str: database connection string
        """

        if ROMM_DB_DRIVER == "mariadb":
            if not DB_USER or not DB_PASSWD:
                log.critical(
                    "Missing database credentials. Please check your configuration file"
                )
                sys.exit(3)

            return (
                f"mariadb+mariadbconnector://{DB_USER}:%s@{DB_HOST}:{DB_PORT}/{DB_NAME}"
                % quote_plus(DB_PASSWD)
            )

        # DEPRECATED
        if ROMM_DB_DRIVER == "sqlite":
            if not os.path.exists(SQLITE_DB_BASE_PATH):
                os.makedirs(SQLITE_DB_BASE_PATH)
            return f"sqlite:////{SQLITE_DB_BASE_PATH}/romm.db"
        # DEPRECATED

        log.critical(f"{ROMM_DB_DRIVER} database not supported")
        sys.exit(3)

    def _parse_config(self):
        """Parses each entry in the config.yml"""

        self.config = Config(
            EXCLUDED_PLATFORMS=pydash.get(self._raw_config, "exclude.platforms", []),
            EXCLUDED_SINGLE_EXT=pydash.get(
                self._raw_config, "exclude.roms.single_file.extensions", []
            ),
            EXCLUDED_SINGLE_FILES=pydash.get(
                self._raw_config, "exclude.roms.single_file.names", []
            ),
            EXCLUDED_MULTI_FILES=pydash.get(
                self._raw_config, "exclude.roms.multi_file.names", []
            ),
            EXCLUDED_MULTI_PARTS_EXT=pydash.get(
                self._raw_config, "exclude.roms.multi_file.parts.extensions", []
            ),
            EXCLUDED_MULTI_PARTS_FILES=pydash.get(
                self._raw_config, "exclude.roms.multi_file.parts.names", []
            ),
            PLATFORMS_BINDING=pydash.get(self._raw_config, "system.platforms", {}),
            ROMS_FOLDER_NAME=pydash.get(
                self._raw_config, "filesystem.roms_folder", "roms"
            ),
            SAVES_FOLDER_NAME=pydash.get(
                self._raw_config, "filesystem.saves_folder", "saves"
            ),
            STATES_FOLDER_NAME=pydash.get(
                self._raw_config, "filesystem.states_folder", "states"
            ),
            SCREENSHOTS_FOLDER_NAME=pydash.get(
                self._raw_config, "filesystem.screenshots_folder", "screenshots"
            ),
        )


config = ConfigLoader().config
