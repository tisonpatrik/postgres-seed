from fastapi import APIRouter, status
from src.handlers.database_handler import DatabaseHandler
from src.api.routes.utils import execute_with_logging

router = APIRouter()
db_handler = DatabaseHandler()

@router.post("/init_tables/", status_code=status.HTTP_200_OK, name="init_tables")
def initialize_tables():
    """Initialize tables in the database."""
    execute_with_logging(db_handler.init_tables,
                               start_msg="Init of tables has started.",
                               end_msg="Init of tables was completed.")
    return {"status": "tables of db were created"}

@router.post("/reset_db/", status_code=status.HTTP_200_OK, name="reset_db")
def reset_database():
    """Reset the database tables."""
    execute_with_logging(db_handler.reset_tables,
                               start_msg="Database table reset started.",
                               end_msg="Database table reset is complete.")
    return {"status": "Database was reset."}
