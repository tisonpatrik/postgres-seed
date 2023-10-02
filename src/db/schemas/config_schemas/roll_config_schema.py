"""
This module defines the schema for configuring the 'roll_config' database table and its associated CSV file.
"""

from src.db.schemas.base_config_schema import BaseConfigSchema


class RollConfigSchema(BaseConfigSchema):
    """
    Concrete class that implements the BaseConfigSchema for the 'roll_config' database table.
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
            "HoldRollCycle": "hold_roll_cycle",
            "RollOffsetDays": "roll_offset_days",
            "CarryOffset": "carry_offset",
            "PricedRollCycle": "priced_roll_cycle",
            "ExpiryOffset": "expiry_offset",
        }

    @property
    def sql_command(self):
        """
        Returns the SQL command to create the 'roll_config' table.

        Returns:
            str: SQL command string.
        """
        return """
                CREATE TABLE roll_config (
                    symbol VARCHAR(50) PRIMARY KEY,
                    hold_roll_cycle VARCHAR(50),
                    roll_offset_days INTEGER,
                    carry_offset INTEGER,
                    priced_roll_cycle VARCHAR(50),
                    expiry_offset INTEGER
                )
                """

    @property
    def table_name(self):
        """
        Returns the name of the 'roll_config' database table.

        Returns:
            str: Name of the database table.
        """
        return "roll_config"

    @property
    def origin_csv_file_path(self):
        """
        Returns the file path of the original CSV file for the 'roll_config' table.

        Returns:
            str: File path of the original CSV.
        """
        return "/path/in/container/csvconfig/rollconfig.csv"
