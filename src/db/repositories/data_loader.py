"""
Module for asynchronous data loading from a database into a Pandas DataFrame.
"""
import logging

import asyncpg
import pandas as pd

from src.db.errors import (
    DatabaseConnectionError,
    DatabaseInteractionError,
    ParameterMismatchError,
    SQLSyntaxError,
    TableOrColumnNotFoundError,
)

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """
    Class responsible for loading data from a database into a Pandas DataFrame.
    """

    def __init__(self, database_url):
        """
        Initialize DataLoader with a database URL.

        Parameters:
            database_url (str): The database URL.
        """
        self.database_url = database_url

    async def fetch_data_as_dataframe_async(self, sql_template, parameters):
        """
        Fetch data from the database using a SQL template and parameters,
        and return it as a Pandas DataFrame.

        Parameters:
            sql_template (str): The SQL template to use for fetching data.
            parameters (dict): The parameters to use with the SQL template.

        Returns:
            pd.DataFrame: The fetched data as a Pandas DataFrame.
        """
        logger.info("Fetching data using provided SQL template.")
        pool = await self._create_connection_pool()
        try:
            rows = await self._execute_sql(pool, sql_template, parameters)
            return self._convert_to_dataframe(rows)
        finally:
            await pool.close()

    async def _create_connection_pool(self):
        try:
            logger.info("Creating connection pool.")
            return await asyncpg.create_pool(dsn=self.database_url)
        except asyncpg.exceptions.ConnectionDoesNotExistError as exc:
            logger.error("Failed to connect to the database.")
            raise DatabaseConnectionError("Failed to connect to the database.") from exc

    async def _execute_sql(self, pool, sql_template, parameters):
        async with pool.acquire() as conn:
            try:
                logger.info("Preparing and executing SQL statement.")
                statement = await conn.prepare(sql_template)
                params_copy = parameters.copy() if parameters else {}
                if "TABLE" not in sql_template and "TABLE" in params_copy:
                    params_copy.pop("TABLE")
                return await statement.fetch(**params_copy)
            except asyncpg.exceptions.UndefinedTableError as exc:
                logger.error("Table or column not defined in SQL: %s", exc)
                raise TableOrColumnNotFoundError(
                    f"Table or column not defined in SQL: {exc}"
                ) from exc
            except asyncpg.exceptions.SyntaxOrAccessError as exc:
                logger.error("Syntax error or access violation in SQL: %s", exc)
                raise SQLSyntaxError(
                    f"Syntax error or access violation in SQL: {exc}"
                ) from exc
            except asyncpg.exceptions.DataError as exc:
                logger.error("Parameter mismatch or data error: %s", exc)
                raise ParameterMismatchError(
                    f"Parameter mismatch or data error: {exc}"
                ) from exc
            except Exception as exc:
                logger.error("Error executing SQL statement: %s", exc)
                raise DatabaseInteractionError(
                    f"Error executing SQL statement: {exc}"
                ) from exc

    def _convert_to_dataframe(self, rows):
        logger.info("Converting fetched rows to DataFrame.")
        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(rows, columns=[desc[0] for desc in rows[0].keys()])
