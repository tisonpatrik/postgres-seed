from fastapi import APIRouter, status

from src.api.routes.utils import execute_with_logging
from src.handlers.config_data_handler import ConfigDataHandler

router = APIRouter()
config_handler = ConfigDataHandler()


@router.post("/parse_files/", status_code=status.HTTP_200_OK, name="parse_files")
def parse_files():
    """Parse files and store them in temp."""
    execute_with_logging(
        config_handler.handle_data_processing,
        start_msg="File parsing started.",
        end_msg="File parsing completed.",
    )
    return {"status": "files were preprocessed and stored in the temp folder"}
