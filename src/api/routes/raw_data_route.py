"""
This module defines the API routes for raw data processing.
It includes a POST endpoint for parsing raw data files and storing them in a temporary location.
"""

from fastapi import APIRouter, status

from src.api.routes.utils import execute_with_logging
from src.handlers.raw_data_handler import RawDataHandler

router = APIRouter()
data_handler = RawDataHandler()


@router.post("/parse_files/", status_code=status.HTTP_200_OK, name="parse_files")
def parse_raw_data_files():
    """Parse raw data files and store them in temp."""
    execute_with_logging(
        data_handler.handle_data_processing,
        start_msg="Raw data file parsing started.",
        end_msg="Raw data file parsing completed.",
    )
    return {"status": "Raw data files were preprocessed and stored in the temp folder"}
