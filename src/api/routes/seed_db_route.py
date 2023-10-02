"""
This module defines the API routes for seeding the database.
It includes a POST endpoint to fill the database tables with data from a temporary folder.
"""

from fastapi import APIRouter, status

from src.api.routes.utils import execute_with_logging_async
from src.core.config import settings
from src.handlers.seed_db_handler import SeedDBHandler

router = APIRouter()
seed_db_handler = SeedDBHandler(settings.database_url)


@router.post("/seed_db/", status_code=status.HTTP_200_OK, name="seed_db")
async def fill_database():
    """Fill the database tables with data."""
    await execute_with_logging_async(
        seed_db_handler.insert_data_from_csv_async,
        start_msg="Database table filling started.",
        end_msg="Database table filling completed.",
    )
    return {"status": "Table was filled with data from temp folder"}
