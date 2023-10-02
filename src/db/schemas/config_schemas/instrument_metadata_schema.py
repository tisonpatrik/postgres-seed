"""
This module defines the schema for configuring the 'instrument_metadata' database table and its associated CSV file.
"""

from src.db.schemas.base_config_schema import BaseConfigSchema


class InstrumentMetadataSchema(BaseConfigSchema):
    """
    Concrete class that implements the BaseConfigSchema for the 'instrument_metadata' database table.
    """

    @property
    def column_mapping(self):
        """
        Returns a dictionary mapping column names to their corresponding database fields.

        Returns:
            Dict[str, str]: A dictionary mapping column names to database fields.
        """
        return {
            "Instrument": "symbol",
            "AssetClass": "asset_class",
            "SubClass": "sub_class",
            "SubSubClass": "sub_sub_class",
            "Style": "style",
            "Country": "country",
            "Duration": "duration",
            "Description": "description",
        }

    @property
    def sql_command(self):
        """
        Returns the SQL command to create the 'instrument_metadata' table.

        Returns:
            str: SQL command string.
        """
        return """
                CREATE TABLE instrument_metadata (
                    symbol VARCHAR(50) PRIMARY KEY,
                    asset_class VARCHAR(50),
                    sub_class VARCHAR(50),
                    sub_sub_class VARCHAR(50),
                    description VARCHAR(100)
                )
                """

    @property
    def table_name(self):
        """
        Returns the name of the 'instrument_metadata' database table.

        Returns:
            str: Name of the database table.
        """
        return "instrument_metadata"

    @property
    def origin_csv_file_path(self):
        """
        Returns the file path of the original CSV file for the 'instrument_metadata' table.

        Returns:
            str: File path of the original CSV.
        """
        return "/path/in/container/csvconfig/moreinstrumentinfo.csv"
