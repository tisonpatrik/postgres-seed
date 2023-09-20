import asyncpg
import pandas as pd
import logging
from src.db.errors import (DatabaseConnectionError, DatabaseInteractionError,
                           SQLSyntaxError, TableOrColumnNotFoundError, ParameterMismatchError)

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, database_url: str):
        self.database_url: str = database_url

    async def fetch_data_as_dataframe_async(self, sql_template: str, parameters: dict = None) -> pd.DataFrame:
        logger.info("Fetching data using provided SQL template.")
        pool = await self._create_connection_pool()
        try:
            rows = await self._execute_sql(pool, sql_template, parameters)
            return self._convert_to_dataframe(rows)
        finally:
            await pool.close()

    async def _create_connection_pool(self) -> asyncpg.pool.Pool:
        try:
            logger.info("Creating connection pool.")
            return await asyncpg.create_pool(dsn=self.database_url)
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            logger.error("Failed to connect to the database.")
            raise DatabaseConnectionError("Failed to connect to the database.")

    async def _execute_sql(self, pool: asyncpg.pool.Pool, sql_template: str, parameters: dict) -> list:
        async with pool.acquire() as conn:
            try:
                logger.info("Preparing and executing SQL statement.")
                statement = await conn.prepare(sql_template)
                
                # Create a copy of parameters to avoid side-effects
                params_copy = parameters.copy() if parameters else {}
                if 'TABLE' not in sql_template and 'TABLE' in params_copy:
                    params_copy.pop('TABLE')
                    
                return await statement.fetch(**params_copy)
                
            except asyncpg.exceptions.UndefinedTableError as e:
                logger.error(f"Table or column not defined in SQL: {e}")
                raise TableOrColumnNotFoundError(f"Table or column not defined in SQL: {e}")
                
            except asyncpg.exceptions.SyntaxOrAccessError as e:
                logger.error(f"Syntax error or access violation in SQL: {e}")
                raise SQLSyntaxError(f"Syntax error or access violation in SQL: {e}")
                
            except asyncpg.exceptions.DataError as e:
                logger.error(f"Parameter mismatch or data error: {e}")
                raise ParameterMismatchError(f"Parameter mismatch or data error: {e}")
                
            except Exception as e:
                logger.error(f"Error executing SQL statement: {e}")
                raise DatabaseInteractionError(f"Error executing SQL statement: {e}")


    def _convert_to_dataframe(self, rows: list) -> pd.DataFrame:
        logger.info("Converting fetched rows to DataFrame.")
        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(rows, columns=[desc[0] for desc in rows[0].keys()])
