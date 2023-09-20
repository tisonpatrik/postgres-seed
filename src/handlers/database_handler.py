import logging

from src.db.repositories.repository import PostgresRepository
from src.db.schemas.schemas import get_schemas

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseHandler:
    def __init__(self, config_schemas: list = None):
        """Initialize the handler with injected or provided config schemas."""
        self.config_schemas = config_schemas if config_schemas else get_schemas()

    def init_tables(self) -> None:
        """
        Initialize tables in the database using schemas.
        """
        repository = PostgresRepository()
        for schema in self.config_schemas:
            repository.create_table(schema.sql_command)

    def reset_tables(self) -> None:
        """
        Reset the database by dropping tables and indexes.
        """
        repository = PostgresRepository()
        try:
            repository.reset_db()
        except Exception as e:
            logger.error(f"Failed to reset the database: {str(e)}")
            raise e
