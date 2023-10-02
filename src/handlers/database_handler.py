"""
Module to handle database operations like table initialization and reset.
"""

import logging

from src.db.repositories.table_creator import TableCreator
from src.db.repositories.table_dropper import TableDropper
from src.db.schemas.schemas import get_schemas
from src.handlers.errors import DatabaseError

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseHandler:
    """
    A class for handling database-related tasks such as table creation and reset.
    """

    def __init__(self, conn):
        """Initialize the handler with schemas fetched from get_schemas."""
        self.config_schemas = get_schemas()
        self.connection = conn

    async def init_tables_async(self) -> None:
        """
        Initialize tables in the database using the SQL commands defined in the schemas.
        """
        creator = TableCreator(self.connection)
        for schema in self.config_schemas:
            try:
                await creator.create_table_async(schema.sql_command)
            except DatabaseError as db_error:  # Catching a more specific exception
                logger.error(
                    "Database error while creating table with SQL command %s: %s",
                    schema.sql_command,
                    db_error,
                )

    async def reset_tables_async(self) -> None:
        """
        Reset the database by dropping tables and indexes.
        """
        dropper = TableDropper(self.connection)
        try:
            await dropper.drop_all_tables_async()
        except DatabaseError as db_error:  # Catching a more specific exception
            logger.error("Database error while resetting the database: %s", db_error)
            raise DatabaseError("Failed to reset the database.") from db_error
