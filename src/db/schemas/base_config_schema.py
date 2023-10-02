"""
This module defines the base schema for configuring database table creation and CSV file paths.
"""

import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)


class BaseConfigSchema(ABC):
    """
    Abstract base class that outlines the schema for configuring database tables and associated CSV files.
    """

    @property
    @abstractmethod
    def column_mapping(self):
        """
        Abstract property that should return a dictionary mapping column names to their data types.

        Returns:
            Dict[str, str]: A dictionary mapping column names to data types.
        """

    @property
    @abstractmethod
    def sql_command(self):
        """
        Abstract property that should return the SQL command to create the table.

        Returns:
            str: SQL command string.
        """

    @property
    @abstractmethod
    def table_name(self):
        """
        Abstract property that should return the name of the database table.

        Returns:
            str: Name of the database table.
        """

    @property
    @abstractmethod
    def origin_csv_file_path(self):
        """
        Abstract property that should return the file path of the original CSV file.

        Returns:
            str: File path of the original CSV.
        """

    @property
    def file_path(self):
        """
        Returns a temporary file path based on the table name.

        Returns:
            str: Temporary file path for CSV.
        """
        return f"/tmp/{self.table_name}.csv"
