"""
This module defines the schema for configuring the 'multiple_prices' database table and its associated CSV file.
"""

from src.db.schemas.base_config_schema import BaseConfigSchema


class MultiplePricesSchema(BaseConfigSchema):
    """
    Concrete class that implements the BaseConfigSchema for the 'multiple_prices' database table.
    """

    @property
    def column_mapping(self):
        """
        Returns a dictionary mapping column names to their corresponding database fields.

        Returns:
            Dict[str, str]: A dictionary mapping column names to database fields.
        """
        return {
            "DATETIME": "unix_date_time",
            "CARRY": "carry",
            "CARRY_CONTRACT": "carry_contract",
            "PRICE": "price",
            "PRICE_CONTRACT": "price_contract",
            "FORWARD": "forward",
            "FORWARD_CONTRACT": "forward_contract",
        }

    @property
    def sql_command(self):
        """
        Returns the SQL command to create the 'multiple_prices' table.

        Returns:
            str: SQL command string.
        """
        return """
            CREATE TABLE multiple_prices (
                    unix_date_time INTEGER,
                    symbol VARCHAR(50),
                    carry FLOAT, 
                    carry_contract INTEGER, 
                    price FLOAT, 
                    price_contract INTEGER, 
                    forward FLOAT, 
                    forward_contract INTEGER,
                    PRIMARY KEY (unix_date_time, symbol)
                )
            """

    @property
    def table_name(self):
        """
        Returns the name of the 'multiple_prices' database table.

        Returns:
            str: Name of the database table.
        """
        return "multiple_prices"

    @property
    def origin_csv_file_path(self):
        """
        Returns the file path of the original CSV file for the 'multiple_prices' table.

        Returns:
            str: File path of the original CSV.
        """
        return "/path/in/container/multiple_prices_csv/"
