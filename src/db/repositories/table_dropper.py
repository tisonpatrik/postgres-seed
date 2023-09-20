import logging

import psycopg2

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TableDropper:
    def __init__(self, database_url: str):
        self.database_url: str = database_url

    def dropAllTables(self):
        """
        Drop all tables and indexes from the connected PostgreSQL database.

        Returns:
        - None
        """
        conn = None
        try:
            # Connect to the PostgreSQL server
            conn = psycopg2.connect(self.database_url)
            cur = conn.cursor()

            # Generate the SQL command to drop all tables
            sql_commands = [
                "DO $$ DECLARE r RECORD; BEGIN FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP EXECUTE 'DROP TABLE IF EXISTS ' || r.tablename || ' CASCADE'; END LOOP; END $$;",
                "DO $$ DECLARE r RECORD; BEGIN FOR r IN (SELECT indexname FROM pg_indexes WHERE schemaname = current_schema()) LOOP EXECUTE 'DROP INDEX IF EXISTS ' || r.indexname || ' CASCADE'; END LOOP; END $$;",
            ]

            for sql_command in sql_commands:
                cur.execute(sql_command)

            # Committing the changes to the database
            conn.commit()

            # Log successful table and index drop
            logger.info(
                f"Successfully dropped all tables and indexes from the database"
            )

            # Close communication with the PostgreSQL database server
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f"Failed to drop tables/indexes due to: {error}")

        finally:
            if conn is not None:
                conn.close()
                logger.info("Database connection closed.")
