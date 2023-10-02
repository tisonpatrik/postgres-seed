"""
This module defines the schema for configuring the 'roll_calendars' database table and its associated CSV file.
"""

from src.db.schemas.base_config_schema import BaseConfigSchema


class RollCalendarsSchema(BaseConfigSchema):
    """
    Concrete class that implements the BaseConfigSchema for the 'roll_calendars' database table.
    """

    @property
    def column_mapping(self):
        """
        Returns a dictionary mapping column names to their corresponding database fields.

        Returns:
            Dict[str, str]: A dictionary mapping column names to database fields.
        """
        return {
            "DATE_TIME": "unix_date_time",
        }

    @property
    def sql_command(self):
        """
        Returns the SQL command to create the 'roll_calendars' table.

        Returns:
            str: SQL command string.
        """
        return """
                CREATE TABLE roll_calendars (
                        unix_date_time INTEGER,
                        symbol VARCHAR(50),
                        current_contract INTEGER,
                        next_contract INTEGER,
                        carry_contract INTEGER,
                        PRIMARY KEY (unix_date_time, symbol)
                    )
                """

    @property
    def table_name(self):
        """
        Returns the name of the 'roll_calendars' database table.

        Returns:
            str: Name of the database table.
        """
        return "roll_calendars"

    @property
    def origin_csv_file_path(self):
        """
        Returns the file path of the original CSV file for the 'roll_calendars' table.

        Returns:
            str: File path of the original CSV.
        """
        return "/path/in/container/roll_calendars_csv/"
