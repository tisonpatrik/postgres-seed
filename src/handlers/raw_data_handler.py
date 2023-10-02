"""
Module to handle raw data processing.
"""

import logging

from src.data_processing.data_preprocessor import (
    process_all_csv_in_directory,
    save_concatenated_dataframes,
)
from src.db.schemas.schemas import get_raw_data_schemas
from src.handlers.errors import ProcessingError

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RawDataHandler:
    """
    Handles raw data processing tasks.
    """

    def __init__(self):
        self.schemas = get_raw_data_schemas()

    def handle_data_processing(self) -> None:
        """
        Processes each configuration schema provided to the handler synchronously.
        This includes loading, transforming, and saving the data for each schema.
        """
        for schema in self.schemas:
            self._process_raw_data_schema(schema)

    def _process_raw_data_schema(self, schema):
        try:
            processed_dataframes = process_all_csv_in_directory(
                schema.origin_csv_file_path, schema.column_mapping
            )
            if processed_dataframes:
                save_concatenated_dataframes(processed_dataframes, schema.file_path)
            else:
                logger.error(
                    "No valid data to save for schema: %s", schema.__class__.__name__
                )
        except FileNotFoundError:
            logger.error(
                "File not found while processing schema: %s", schema.__class__.__name__
            )
        except KeyError:
            logger.error(
                "KeyError occurred while processing schema: %s",
                schema.__class__.__name__,
            )
        except ValueError:
            logger.error(
                "ValueError occurred while processing schema: %s",
                schema.__class__.__name__,
            )
        except ProcessingError as error:  # Keeping a general Exception as a last resort
            logger.error(
                "An unidentified error occurred while processing the schema: %s", error
            )
