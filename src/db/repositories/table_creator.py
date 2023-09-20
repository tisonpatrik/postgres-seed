import logging
import psycopg2

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TableCreator:
    def __init__(self, database_url: str):
        self.database_url: str = database_url

    def create_table(self, sql_command: str):
        """
        Create a table in the PostgreSQL database based on the provided SQL command.
        
        Args:
        - sql_command (str): SQL command to create a table.
        
        Returns:
        - None
        """
        conn = None
        try:
            # Connect to the PostgreSQL server
            conn = psycopg2.connect(self.database_url)
            cur = conn.cursor()
            
            # Execute the SQL command to create the table
            cur.execute(sql_command)
            
            # Commit the changes
            conn.commit()
            
            # Log successful table creation
            logger.info(f"Successfully executed the following SQL command: {sql_command}")
            
            # Close communication with the PostgreSQL database server
            cur.close()
            
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f"Failed to execute the SQL command due to: {error}")
            
        finally:
            if conn is not None:
                conn.close()
                logger.info("Database connection closed.")