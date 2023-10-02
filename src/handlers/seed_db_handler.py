"""
This module contains the SeedDBHandler class, which is responsible for seeding the database from CSV files.
"""

import asyncio
import logging

from src.data_processing.csv_helper import load_csv
from src.db.repositories.data_inserter import DataInserter
from src.db.schemas.base_config_schema import BaseConfigSchema
from src.db.schemas.schemas import get_schemas

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SeedDBHandler:
    """
    This class provides methods to seed the database asynchronously from CSV files according to given schemas.
    """

    def __init__(self, database_url):
        """
        Initialize the SeedDBHandler with database URL and fetch all relevant schemas.
        """
        self.schemas = get_schemas()
        self.database_url = database_url

    async def insert_data_from_csv_async(self):
        """
        Asynchronously seed the database from CSV files using predefined schemas.
        """
        tasks = [
            self._load_csv_and_insert_data_to_db_async(schema)
            for schema in self.schemas
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                logger.error("Error occurred while inserting data from CSV: %s", result)

    async def _load_csv_and_insert_data_to_db_async(self, schema: BaseConfigSchema):
        """
        Asynchronously load data from a CSV file and insert it into the database as specified by the schema.
        """
        data_seeder = DataInserter(self.database_url)
        try:
            data_frame = load_csv(schema.file_path)
            await data_seeder.insert_dataframe_async(data_frame, schema.table_name)
        except Exception as error:
            logger.error(
                "Error occurred while processing the CSV file %s: %s",
                schema.file_path,
                error,
            )
            raise error
