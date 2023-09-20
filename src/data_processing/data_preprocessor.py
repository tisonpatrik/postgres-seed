import logging
import os
from typing import List

import pandas as pd

from src.data_processing.csv_helper import load_csv
from src.data_processing.data_frame_helper import (
    add_symbol_by_file_name,
    aggregate_to_day_based_prices,
    convert_datetime_to_unixtime,
    rename_columns_if_needed,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_and_rename_columns(
    file_path: str, column_mapping: dict = None
) -> pd.DataFrame:
    """
    Load and process the CSV data from the given path and rename the columns.

    Args:
        file_path (str): Path to the source CSV file.
        column_mapping (dict, optional): Mapping for renaming columns.

    Returns:
        pd.DataFrame: Processed data.
    """
    try:
        df = load_csv(file_path)
        df = rename_columns_if_needed(df, column_mapping)
        logger.info(f"Successfully loaded and renamed columns for {file_path}.")
        return df

    except Exception as e:
        logger.error(f"Error processing data from {file_path}: {e}")
        raise


def load_all_csv_files_from_directory(directory_path: str) -> List[pd.DataFrame]:
    """
    Loads all CSV files from a directory, extracts the symbol from the filename,
    and appends it to each dataframe.

    Args:
        directory_path (str): Path to the directory containing the CSV files.

    Returns:
        List[pd.DataFrame]: List of DataFrames with appended symbol columns.
    """
    dataframes = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory_path, file_name)
            try:
                loaded = load_csv(file_path)
                date_time = loaded.columns[0]
                price = loaded.columns[1]
                agregated = aggregate_to_day_based_prices(
                    loaded, index_column=date_time, price_column=price
                )
                coverted = convert_datetime_to_unixtime(agregated, date_time)
                df = add_symbol_by_file_name(coverted, file_path)
                dataframes.append(df)
                logger.info(f"Successfully loaded and added symbol for {file_path}.")
            except Exception as e:
                logger.error(f"Error loading data from {file_path}: {e}")

    return dataframes
