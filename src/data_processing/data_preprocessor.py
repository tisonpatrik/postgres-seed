"""
Module for preprocessing CSV data.

This module provides functions for loading, preprocessing, and handling CSV data.
It enables renaming of columns, aggregation of data, and other preparatory operations
for downstream analyses.
"""

import logging
import os

from src.data_processing.csv_helper import load_csv, save_to_csv
from src.data_processing.data_frame_helper import (
    add_symbol_by_file_name,
    aggregate_to_day_based_prices,
    concat_dataframes,
    convert_datetime_to_unixtime,
    rename_columns,
)
from src.data_processing.errors import ProcessingError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_and_process_raw_data_csv(file_path, column_mapping, file_name):
    """
    Loads and processes raw data from a CSV file.

    Parameters:
        file_path (str): The path to the CSV file.
        column_mapping (dict): A mapping from old column names to new column names.
        file_name (str): The name of the file, used to add a 'symbol' column.

    Returns:
        pd.DataFrame or None: A DataFrame containing the processed data, or None if an error occurs.
    """
    try:
        data_frame = load_csv(file_path)
        data_frame = rename_columns(data_frame, column_mapping)
        # Check if 'price' column is present before aggregation
        if "price" in data_frame.columns:
            data_frame = aggregate_to_day_based_prices(data_frame)

        data_frame = convert_datetime_to_unixtime(data_frame)
        data_frame = add_symbol_by_file_name(data_frame, file_name)
        return data_frame
    except ProcessingError as error:  # Renamed 'e' to 'error'
        logger.error(
            "Error processing %s: %s", file_path, error
        )  # Changed to lazy formatting
        return None


def process_all_csv_in_directory(directory_path, column_mapping):
    """
    Processes all CSV files in a given directory.

    Parameters:
        directory_path (str): The path to the directory containing CSV files.
        column_mapping (dict): A mapping from old column names to new column names.

    Returns:
        list: A list of processed DataFrames.
    """
    processed_dfs = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory_path, file_name)
            processed_df = load_and_process_raw_data_csv(
                file_path, column_mapping, os.path.splitext(file_name)[0]
            )
            if processed_df is not None:
                processed_dfs.append(processed_df)
    return processed_dfs


def save_concatenated_dataframes(data_frames, save_path):
    """
    Concatenates a list of DataFrames and saves the result to a CSV file.

    Parameters:
        data_frames (list): A list of DataFrames to concatenate.
        save_path (str): The path to save the concatenated DataFrame.
    """
    concatenated_df = concat_dataframes(data_frames)
    drop_unnamed_column(concatenated_df)
    save_to_csv(concatenated_df, save_path)


def drop_unnamed_column(data_frame):
    """
    Drops the column 'Unnamed: 4' from the DataFrame if it exists.
    """
    if "Unnamed: 4" in data_frame.columns:
        data_frame.drop("Unnamed: 4", axis=1, inplace=True)
    return data_frame
