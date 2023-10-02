"""
Module to handle configuration data processing.
"""

import logging

from src.data_processing.csv_helper import save_to_csv
from src.data_processing.data_frame_helper import fill_empty_values
from src.data_processing.data_preprocessor import load_csv, rename_columns
from src.db.schemas.schemas import get_configs_schemas
from src.handlers.errors import ProcessingError

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigDataHandler:
    """
    Initializes the ConfigDataHandler with the given schemas, or defaults if none provided.

    Parameters:
    - schemas: List of configuration schemas to be processed.
    """

    def __init__(self):
        self.schemas = get_configs_schemas()

    def handle_data_processing(self) -> None:
        """
        Processes each configuration schema provided to the handler synchronously.
        This includes loading, transforming, and saving the data for each schema.
        """
        results = [self._process_config_schema(schema) for schema in self.schemas]
        for schema, result in zip(self.schemas, results):
            if isinstance(result, Exception):
                logger.error(
                    "Error processing data for schema %s: %s",
                    schema.__class__.__name__,
                    result,
                )

    def _process_config_schema(self, schema):
        """
        Processes a single configuration schema synchronously.
        This includes loading the data from the specified CSV file, transforming the data
        according to the given schema, and then saving the transformed data back to the same CSV file.

        If any error occurs during processing, logs an error message with details and returns the exception.

        Parameters:
        - schema: The configuration schema detailing how the data should be processed.
        """
        try:
            data = load_csv(schema.origin_csv_file_path)
            renamed = rename_columns(data, schema.column_mapping)
            filled = fill_empty_values(
                renamed, fill_value=0
            )  # Assuming you want to fill with 0
            save_to_csv(filled, schema.file_path)
            logger.info(
                "Data processing completed for schema: %s", schema.__class__.__name__
            )
            return True
        except Exception as error:  # More specific exceptions are advisable
            logger.error(
                "Error processing data for schema %s: %s",
                schema.__class__.__name__,
                error,
            )
            raise ProcessingError from error
