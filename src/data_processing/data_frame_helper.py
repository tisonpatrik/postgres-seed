"""
Data Frame Helper module.

This module provides utility functions to preprocess and transform pandas DataFrames. 
It provides functions to rename columns, handle empty values, add symbols, convert 
datetime columns to UNIX timestamp, and aggregate raw prices to daily averages.
"""

import logging

import pandas as pd

from src.data_processing.errors import (
    ColumnRenameError,
    DataAggregationError,
    DateTimeConversionError,
    DuplicateRowsError,
    EmptyValueFillError,
    InvalidDatetimeColumnError,
    SymbolAdditionError,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def rename_columns(data_frame, new_column_names):
    """
    Renames DataFrame columns based on the provided dictionary.
    """
    missing_columns = set(new_column_names.keys()) - set(data_frame.columns)
    if missing_columns:
        missing_columns_str = ", ".join(missing_columns)
        logger.error("Columns %s do not exist in the DataFrame", missing_columns_str)
        raise ColumnRenameError(f"Columns {missing_columns_str} do not exist")
    try:
        return data_frame.rename(columns=new_column_names)
    except Exception as error:
        logger.error("Error during column renaming: %s", error)
        raise ColumnRenameError from error


def fill_empty_values(data_frame, fill_value):
    """
    Fills empty values in the DataFrame with the provided fill_value.
    """
    if isinstance(fill_value, dict):
        missing_columns = set(fill_value.keys()) - set(data_frame.columns)
        if missing_columns:
            raise EmptyValueFillError(
                f"Columns {', '.join(missing_columns)} do not exist"
            )

    try:
        return data_frame.fillna(fill_value)
    except Exception as error:
        logger.error("Error during filling empty values: %s", error)
        raise EmptyValueFillError from error


def add_symbol_by_file_name(data_frame, symbol):
    """
    Adds a 'symbol' column to the DataFrame with the provided symbol.
    """
    try:
        data_frame["symbol"] = symbol
        return data_frame
    except Exception as error:
        logger.error("Error during symbol addition: %s", error)
        raise SymbolAdditionError from error


def convert_datetime_to_unixtime(data_frame):
    """
    Converts the date_column to UNIX time.
    """
    try:
        data_frame["unix_date_time"] = (
            pd.to_datetime(data_frame["unix_date_time"]).astype(int) // 10**9
        )
        data_frame = data_frame.dropna()
        return data_frame
    except Exception as error:
        logger.error("Error during date-time conversion: %s", error)
        raise DateTimeConversionError from error


def aggregate_to_day_based_prices(data_frame):
    """
    Aggregates the time-based price data to daily averages.

    Parameters:
        data_frame: DataFrame containing 'unix_date_time' and 'price' columns

    Returns:
        DataFrame: Aggregated DataFrame with daily average prices.
    """
    try:
        converted_date = convert_column_to_datetime(data_frame, "unix_date_time")
        # Set DATETIME as index
        converted_date.set_index("unix_date_time", inplace=True)
        # Resample to daily frequency using the mean of the prices for each day
        result = converted_date.resample("D").mean().dropna().reset_index()
        # Round the price to 1 decimal place
        result["price"] = result["price"].round(1)
        return result
    except Exception as error:
        logger.error("Error during data aggregation: %s", error)
        raise DataAggregationError from error


def convert_column_to_datetime(data_frame, column_name):
    """
    Converts a specified column in the DataFrame to datetime format.

    Parameters:
        data_frame (pd.DataFrame): The DataFrame containing the column to convert.
        column_name (str): The name of the column to convert to datetime.

    Returns:
        pd.DataFrame: A new DataFrame with the specified column converted to datetime.
    """
    new_df = data_frame.copy()  # Create a new DataFrame
    try:
        # Ensure the column is of a datetime type
        new_df[column_name] = pd.to_datetime(new_df[column_name], errors="coerce")
        # Check for any NA/NaN values in the column
        if new_df[column_name].isna().any():
            raise InvalidDatetimeColumnError(
                f"Failed to convert all values in '{column_name}' to datetime."
            )
    except Exception as exc:
        logger.error(
            "Error converting column '%s' to datetime: %s", column_name, str(exc)
        )
        raise
    return new_df


def concat_dataframes(data_frames):
    """
    Concatenates a list of pandas DataFrames, resetting the index and checking for duplicate rows.

    Parameters:
        data_frames (list of pd.DataFrame): List of DataFrames to concatenate.

    Returns:
        pd.DataFrame: A new DataFrame resulting from the concatenation of the input DataFrames.

    Raises:
        DuplicateRowsError: If duplicate rows are found based on 'unix_date_time' and 'symbol'.
    """
    concatenated_df = pd.concat(data_frames, ignore_index=True)
    # Check for duplicate rows based on 'unix_date_time' and 'symbol'
    duplicate_rows = concatenated_df.duplicated(
        subset=["unix_date_time", "symbol"], keep=False
    )
    if any(duplicate_rows):
        raise DuplicateRowsError(
            f"Found duplicate rows based on 'unix_date_time' and 'symbol': {concatenated_df[duplicate_rows]}"
        )
    return concatenated_df
