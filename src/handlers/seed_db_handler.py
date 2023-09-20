import logging
from typing import List
from src.db.schemas.schemas import get_schemas
from src.db.schemas.base_config_schema import BaseConfigSchema
from src.data_processing.csv_helper import load_csv
from src.db.repositories.repository import PostgresRepository 
import asyncio

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeedDBHandler:
    def __init__(self, 
                 schemas: List[BaseConfigSchema] = None, 
                 repository: PostgresRepository = None):
        """
        Initializes the SeedDBHandler with the given schemas and database repository, 
        or defaults if none provided.
        
        Parameters:
        - schemas: List of configuration schemas to be processed.
        - repository: Repository for database operations.
        """
        self.schemas = schemas if schemas else get_schemas()
        self.repository = repository if repository else PostgresRepository()


    async def insert_data_from_csv_async(self) -> None:
        """
        Asynchronously inserts data from CSV files into the database for all given schemas.
        
        This involves loading the data from each CSV file and inserting it into the database according to the table name
        specified in each schema.
        """
        tasks = [self._load_csv_and_insert_data_to_db_async(schema) for schema in self.schemas]
        results = await asyncio.gather(*tasks, return_exceptions=True) # Change here to capture exceptions

        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Error occurred while inserting data from CSV: {result}")

    async def _load_csv_and_insert_data_to_db_async(self, schema: BaseConfigSchema) -> None:
        """
        Asynchronously loads data from a CSV file specified in a given schema and inserts it into the database.
        
        Parameters:
        - schema: The configuration schema detailing the CSV file path and target table name.
        """
        try:
            df = load_csv(schema.file_path)
            await self.repository.insert_data_async(df, schema.table_name)
        except Exception as e:
            logger.error(f"Error occurred while processing the CSV file {schema.file_path}: {e}")
            raise e  # Re-raise the exception for the gather method to capture