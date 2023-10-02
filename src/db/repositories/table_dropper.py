"""
This module contains a class for dropping all tables and indexes from a PostgreSQL database.
"""
import logging

import asyncpg

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TableDropper:
    """
    Represents an interface to drop all tables and indexes from a PostgreSQL database.
    """

    def __init__(self, database_url):
        self.database_url = database_url

    async def drop_all_tables_async(self):
        """
        Drop all tables and indexes from the connected PostgreSQL database.

        Returns:
        - None
        """
        # Generate the SQL command to drop all tables
        drop_tables_command = (
            "DO $$ DECLARE r RECORD; "
            "BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) "
            "LOOP EXECUTE 'DROP TABLE IF EXISTS ' || r.tablename || ' CASCADE'; "
            "END LOOP; END $$;"
        )

        drop_indexes_command = (
            "DO $$ DECLARE r RECORD; "
            "BEGIN FOR r IN (SELECT indexname FROM pg_indexes WHERE schemaname = current_schema()) "
            "LOOP EXECUTE 'DROP INDEX IF EXISTS ' || r.indexname || ' CASCADE'; "
            "END LOOP; END $$;"
        )

        # Connect to the database
        conn = await asyncpg.connect(self.database_url)

        try:
            async with conn.transaction():
                await conn.execute(drop_tables_command)
                await conn.execute(drop_indexes_command)
        finally:
            await conn.close()

        logger.info("Successfully dropped all tables and indexes from the database")
