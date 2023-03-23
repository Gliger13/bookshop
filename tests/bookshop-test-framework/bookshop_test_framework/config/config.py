"""Tests config

Module contains testing config for bookshop application.
"""
import inspect
import os
from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from functools import lru_cache
from importlib.resources import files
from typing import Optional

import yaml


class Environment(Enum):
    """Describes all environment types"""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


@dataclass(repr=False, frozen=True, kw_only=True, slots=True)
class Config:
    """Testing config"""

    environment: str
    base_url: str
    role_name_id_map: dict[str, int] = field(default_factory=dict)
    status_name_id_map: dict[str, int] = field(default_factory=dict)
    additional_config: dict = field(default_factory=dict)


class BaseConfigLoader(metaclass=ABCMeta):
    def __init__(self, loader_config: Optional[dict] = None) -> None:
        self._loader_config = loader_config

    @lru_cache
    def get_config(self) -> Config:
        raw_config = self._load_config()

        current_environment_name = self._get_current_environment_name()
        current_environment_config = raw_config.get(current_environment_name, {})
        merged_config = raw_config.get("common", {})
        merged_config.update(current_environment_config)

        required_config_keys = set(inspect.getfullargspec(Config).kwonlyargs)
        required_config = {key: value for key, value in merged_config.items() if key in required_config_keys}
        additional_config_keys = set(merged_config.keys()) - required_config_keys
        additional_config = {config_key: merged_config[config_key] for config_key in additional_config_keys}
        return Config(environment=current_environment_name, **required_config, additional_config=additional_config)

    @abstractmethod
    def _load_config(self) -> dict:
        """Abstract method to return raw environment config"""

    @abstractmethod
    def _get_current_environment_name(self) -> str:
        """Abstract method to get current environment name"""


class YamlConfigLoader(BaseConfigLoader):
    def _load_config(self) -> dict:
        config_path = str(files("bookshop_test_framework.config").joinpath("config.yaml"))
        with open(config_path, encoding="utf-8") as yaml_confi:
            return yaml.safe_load(yaml_confi)

    def _get_current_environment_name(self) -> str:
        return Environment(os.getenv("ENV", "").lower()).value


def get_config() -> Config:
    """Testing config factory method

    :return: loaded and parsed testing config
    """
    config_loader = YamlConfigLoader()
    return config_loader.get_config()


class BookshopUiEndpoints:
    """Contains UI page endpoints"""

    REGISTRATION_PAGE = "registration"
    PRODUCTS_PAGE = "products"
    USER_PAGE = "user"
