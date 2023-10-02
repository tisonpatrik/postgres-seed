"""
This module defines the API routes for database interactions.
It includes POST endpoints for initializing and resetting database tables.
"""

from fastapi import APIRouter, status

from src.api.routes.utils import execute_with_logging_async
from src.core.config import settings
from src.handlers.database_handler import DatabaseHandler

router = APIRouter()
db_handler = DatabaseHandler(settings.database_url)


@router.post("/init_tables/", status_code=status.HTTP_200_OK, name="init_tables")
async def initialize_tables():
    """Initialize tables in the database."""
    await execute_with_logging_async(
        db_handler.init_tables_async,
        start_msg="Init of tables has started.",
        end_msg="Init of tables was completed.",
    )
    return {"status": "tables of db were created"}


@router.post("/reset_db/", status_code=status.HTTP_200_OK, name="reset_db")
async def reset_database():
    """Reset the database tables."""
    await execute_with_logging_async(
        db_handler.reset_tables_async,
        start_msg="Database table reset started.",
        end_msg="Database table reset is complete.",
    )
    return {"status": "Database was reset."}
