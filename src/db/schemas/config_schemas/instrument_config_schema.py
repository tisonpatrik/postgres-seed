"""
This module defines the schema for configuring the 'instrument_config' database table and its associated CSV file.
"""

from src.db.schemas.base_config_schema import BaseConfigSchema


class InstrumentConfigSchema(BaseConfigSchema):
    """
    Concrete class that implements the BaseConfigSchema for the 'instrument_config' database table.
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
            "Description": "description",
            "Pointsize": "pointsize",
            "Currency": "currency",
            "AssetClass": "asset_class",
            "PerBlock": "per_block",
            "Percentage": "percentage",
            "PerTrade": "per_trade",
            "Region": "region",
        }

    @property
    def sql_command(self):
        """
        Returns the SQL command to create the 'instrument_config' table.

        Returns:
            str: SQL command string.
        """
        return """
                CREATE TABLE instrument_config (
                        symbol VARCHAR(50) PRIMARY KEY, 
                        description TEXT, 
                        pointsize FLOAT, 
                        currency VARCHAR(10), 
                        asset_class VARCHAR(50), 
                        per_block FLOAT, 
                        percentage FLOAT, 
                        per_trade INTEGER, 
                        region VARCHAR(50)
                    )
                """

    @property
    def table_name(self):
        """
        Returns the name of the 'instrument_config' database table.

        Returns:
            str: Name of the database table.
        """
        return "instrument_config"

    @property
    def origin_csv_file_path(self):
        """
        Returns the file path of the original CSV file for the 'instrument_config' table.

        Returns:
            str: File path of the original CSV.
        """
        return "/path/in/container/csvconfig/instrumentconfig.csv"
