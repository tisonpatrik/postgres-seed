"""
This module defines the schema for configuring the 'adjusted_prices' database table and its associated CSV file.
"""

from src.db.schemas.base_config_schema import BaseConfigSchema


class AdjustedPricesSchema(BaseConfigSchema):
    """
    Concrete class that implements the BaseConfigSchema for the 'adjusted_prices' database table.
    """

    @property
    def column_mapping(self):
        """
        Returns a dictionary mapping column names to their corresponding database fields.

        Returns:
            Dict[str, str]: A dictionary mapping column names to database fields.
        """
        return {"DATETIME": "unix_date_time", "price": "price"}

    @property
    def sql_command(self):
        """
        Returns the SQL command to create the 'adjusted_prices' table.

        Returns:
            str: SQL command string.
        """
        return """
                CREATE TABLE adjusted_prices (
                        unix_date_time INTEGER,
                        symbol VARCHAR(50),
                        price FLOAT,
                        PRIMARY KEY (unix_date_time, symbol)
                    )
                """

    @property
    def table_name(self):
        """
        Returns the name of the 'adjusted_prices' database table.

        Returns:
            str: Name of the database table.
        """
        return "adjusted_prices"

    @property
    def origin_csv_file_path(self):
        """
        Returns the file path of the original CSV file for the 'adjusted_prices' table.

        Returns:
            str: File path of the original CSV.
        """
        return "/path/in/container/adjusted_prices_csv/"
