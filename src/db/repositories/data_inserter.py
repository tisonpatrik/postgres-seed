"""
This module provides functionalities for inserting data into a database asynchronously.
"""
import logging
from contextlib import asynccontextmanager

import asyncpg

from src.db.errors import (
    DatabaseConnectionError,
    DatabaseInteractionError,
    TableOrColumnNotFoundError,
)

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataInserter:
    """
    Class for inserting data into a database table asynchronously.
    """

    def __init__(self, database_url):
        """
        Initialize the DataInserter with a database URL.

        Parameters:
            database_url (str): URL of the database to connect to.
        """
        self._database_url = database_url

    async def insert_dataframe_async(self, data_frame, table_name) -> None:
        """
        Insert a Pandas DataFrame into a database table asynchronously.

        Parameters:
            data_frame (pd.DataFrame): The DataFrame to insert.
            table_name (str): The name of the database table to insert into.
        """
        async with self._create_connection_pool_async() as pool:
            await self._bulk_insert_async(pool, data_frame, table_name)

    @asynccontextmanager
    async def _create_connection_pool_async(self):
        logger.info("Creating connection pool.")
        try:
            pool = await asyncpg.create_pool(dsn=self._database_url)
            yield pool
        except asyncpg.exceptions.ConnectionDoesNotExistError as exc:
            logger.error("Failed to connect to the database.")
            raise DatabaseConnectionError("Failed to connect to the database.") from exc
        finally:
            await pool.close()

    async def _bulk_insert_async(self, pool, data_frame, table_name):
        async with pool.acquire() as conn:
            try:
                await self._insert_records_async(conn, data_frame, table_name)
            except asyncpg.exceptions.UndefinedTableError as exc:
                logger.error("Table or column not defined in SQL: %s", exc)
                raise TableOrColumnNotFoundError(
                    f"Table or column not defined in SQL: {exc}"
                ) from exc
            except Exception as exc:
                logger.error("Error inserting data: %s", exc)
                raise DatabaseInteractionError(f"Error inserting data: {exc}") from exc

    async def _insert_records_async(self, conn, data_frame, table_name):
        records = data_frame.values.tolist()
        columns = data_frame.columns.tolist()
        await conn.copy_records_to_table(table_name, records=records, columns=columns)
