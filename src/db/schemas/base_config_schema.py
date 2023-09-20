import logging
from abc import ABC, abstractmethod
from typing import Dict

logging.basicConfig(level=logging.INFO)


class BaseConfigSchema(ABC):
    @property
    @abstractmethod
    def column_mapping(self) -> Dict[str, str]:
        pass

    @property
    @abstractmethod
    def sql_command(self) -> str:
        pass

    @property
    @abstractmethod
    def table_name(self) -> str:
        pass

    @property
    @abstractmethod
    def origin_csv_file_path(self) -> str:
        pass

    @property
    def file_path(self) -> str:
        return f"/tmp/{self.table_name}.csv"
