import logging
import os
import pandas as pd
from typing import List
from src.db.schemas.schemas import get_raw_data_schemas
from src.db.schemas.base_config_schema import BaseConfigSchema
from src.data_processing.data_preprocessor import load_all_csv_files_from_directory
from src.data_processing.csv_helper import save_to_csv
from src.data_processing.data_frame_helper import rename_columns_if_needed

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RawDataHandler:
    def __init__(self, schemas: List[BaseConfigSchema] = None):
        """
        Initializes the RawDataHandler with provided schemas or defaults.

        Parameters:
        - schemas: List of raw data schemas to be processed.
        """
        self.schemas = schemas if schemas else get_raw_data_schemas()

    def handle_data_processing(self) -> None:
        """
        Processes each configuration schema provided to the handler synchronously.
        This includes loading, transforming, and saving the data for each schema.
        """
        results = [self._process_raw_data_schema(schema) for schema in self.schemas]

        # Log any exceptions that occurred during processing
        for schema, result in zip(self.schemas, results):
            if isinstance(result, Exception):
                logger.error(f"Error processing data for schema {schema.__class__.__name__}: {result}")

    def _process_raw_data_schema(self, schema: BaseConfigSchema) -> None:
        # Ensure directory exists
        if not os.path.isdir(schema.origin_csv_file_path):
            logger.warning(f"Directory not found: {schema.origin_csv_file_path}")
            return

        dataframes = load_all_csv_files_from_directory(schema.origin_csv_file_path)

        # Return if no valid CSV files were found or loaded
        if not dataframes:
            logger.warning(f"No valid CSV files found in {schema.origin_csv_file_path}")
            return

        if not self._process_and_save_dataframes(dataframes, schema):
            logger.error(f"Failed to process and save data for schema: {schema.__class__.__name__}")
    
    def _process_and_save_dataframes(self, dataframes: List[pd.DataFrame], schema: BaseConfigSchema) -> bool:
        """
        Concatenates and processes a list of dataframes and saves the result to a specified path.

        Parameters:
        - dataframes: List of DataFrames to be processed.
        - save_path: Path to save the processed data.

        Returns:
        - True if processing was successful, False otherwise.
        """
        try:
            df = pd.concat(dataframes, ignore_index=True)
            
            # Drop columns that have 'Unnamed' in their name
            df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col])
            
            renamed = rename_columns_if_needed(df, schema.column_mapping)
            save_to_csv(renamed, schema.file_path)
            return True
        except Exception as e:
            logger.error(f"Error during concatenation or data processing: {e}")
            return False