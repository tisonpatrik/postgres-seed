"""
This module defines the schema for configuring the 'spread_cost' database table and its associated CSV file.
"""

from src.db.schemas.base_config_schema import BaseConfigSchema


class SpreadCostSchema(BaseConfigSchema):
    """
    Concrete class that implements the BaseConfigSchema for the 'spread_cost' database table.
    """

    @property
    def column_mapping(self):
        """
        Returns a dictionary mapping column names to their corresponding database fields.

        Returns:
            Dict[str, str]: A dictionary mapping column names to database fields.
        """
        return {"Instrument": "symbol", "SpreadCost": "spread_cost"}

    @property
    def sql_command(self):
        """
        Returns the SQL command to create the 'spread_cost' table.

        Returns:
            str: SQL command string.
        """
        return """
                CREATE TABLE spread_cost (
                    symbol VARCHAR(50) PRIMARY KEY,
                    spread_cost FLOAT
                )
                """

    @property
    def table_name(self):
        """
        Returns the name of the 'spread_cost' database table.

        Returns:
            str: Name of the database table.
        """
        return "spread_cost"

    @property
    def origin_csv_file_path(self):
        """
        Returns the file path of the original CSV file for the 'spread_cost' table.

        Returns:
            str: File path of the original CSV.
        """
        return "/path/in/container/csvconfig/spreadcosts.csv"
