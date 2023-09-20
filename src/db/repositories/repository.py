import logging

import pandas as pd

from src.core.config import settings
from src.db.repositories.data_inserter import DataInserter
from src.db.repositories.data_loader import DataLoader
from src.db.repositories.table_creator import TableCreator
from src.db.repositories.table_dropper import TableDropper

logger = logging.getLogger(__name__)


class PostgresRepository:
    def __init__(self):
        self.database_url: str = settings.sync_database_url
        self.inserter = DataInserter(self.database_url)
        self.loader = DataLoader(self.database_url)
        self.creator = TableCreator(self.database_url)
        self.dropper = TableDropper(self.database_url)

    async def insert_data_async(self, df: pd.DataFrame, table_name: str) -> None:
        """
        Asynchronously inserts data from a DataFrame into a specified table.

        Args:
        - df: The DataFrame containing the data to insert.
        - table_name: The name of the table where the data will be inserted.
        """
        try:
            await self.inserter.insert_dataframe_async(df, table_name)
        except Exception as e:
            logger.error(f"Error inserting data into {table_name}: {e}")
            raise

    async def load_data_async(
        self, sql_template: str, parameters: dict = None
    ) -> pd.DataFrame:
        """
        Asynchronously loads data based on the provided SQL template and parameters.

        Args:
        - sql_template: The SQL query template.
        - parameters: A dictionary of parameters to be used in the SQL template.

        Returns:
        A DataFrame containing the loaded data.
        """
        try:
            return await self.loader.fetch_data_as_dataframe_async(
                sql_template, parameters
            )
        except Exception as e:
            logger.error(f"Error loading data with SQL template {sql_template}: {e}")
            raise

    def create_table(self, sql_command: str) -> None:
        """
        Creates a table in the database using the provided SQL command.

        Args:
        - sql_command: The SQL command to create a table.
        """
        try:
            self.creator.create_table(sql_command=sql_command)
        except Exception as e:
            logger.error(f"Error creating table with SQL command {sql_command}: {e}")
            raise

    def reset_db(self) -> None:
        """Drops all tables in the database to reset it."""
        try:
            self.dropper.dropAllTables()
        except Exception as e:
            logger.error(f"Error resetting the database: {e}")
            raise
