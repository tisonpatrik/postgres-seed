import logging
import os

import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def rename_columns_if_needed(
    df: pd.DataFrame, column_mapping: dict = None
) -> pd.DataFrame:
    """Rename DataFrame columns based on the provided column mapping."""
    if column_mapping:
        df.rename(columns=column_mapping, inplace=True)
        logger.info("Columns renamed according to provided mapping.")
    return df


def fill_empty_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle empty values within the DataFrame."""
    df.fillna("", inplace=True)  # inplace=True for inplace operation
    df = df.applymap(lambda x: "" if x == "" else x)
    return df


def add_symbol_by_file_name(df: pd.DataFrame, file_path: str) -> pd.DataFrame:
    """
    Adds a 'symbol' column to the DataFrame by extracting the file name from the provided file path.

    Args:
        df (pd.DataFrame): Input DataFrame.
        file_path (str): Path to the file.

    Returns:
        pd.DataFrame: DataFrame with appended symbol column.
    """
    try:
        # Extract the file name (without extension) from the file path
        symbol = os.path.splitext(os.path.basename(file_path))[0]

        # Add the 'symbol' column to the DataFrame
        df["symbol"] = symbol

        logger.info(
            f"Successfully added symbol '{symbol}' from file path '{file_path}'."
        )

    except Exception as e:
        logger.error(f"Error adding symbol from file path '{file_path}': {e}")
        raise

    return df


def convert_datetime_to_unixtime(df: pd.DataFrame, date_time_name: str) -> pd.DataFrame:
    """
    Convert a datetime column in the DataFrame to UNIX timestamp.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column to be converted.

    Returns:
        pd.DataFrame: DataFrame with the column converted to UNIX timestamp.
    """
    try:
        # Convert the column to datetime format
        df[date_time_name] = pd.to_datetime(df[date_time_name])
        # Convert the datetime format to UNIX timestamp
        df[date_time_name] = df[date_time_name].apply(lambda x: int(x.timestamp()))
        logger.info(
            f"Successfully converted column '{date_time_name}' to UNIX timestamp."
        )
        return df

    except Exception as e:
        logger.error(
            f"Error converting column '{date_time_name}' to UNIX timestamp: {e}"
        )
        raise


def aggregate_to_day_based_prices(
    df: pd.DataFrame, index_column: str, price_column: str
) -> pd.DataFrame:
    """
    Convert a dictionary of raw prices to a DataFrame, set a datetime index,
    and aggregate to provide average daily prices.

    Args:
        df (pd.DataFrame): DataFrame of raw prices.
        index_column (str): The name of the column to be used as the index.
        price_column (str): The name of the column containing the price values.

    Returns:
        pd.DataFrame: DataFrame with dates as index and daily average prices.
    """
    try:
        # Set datetime index
        df[index_column] = pd.to_datetime(df[index_column])
        df.set_index(index_column, inplace=True)

        # Ensure price column is in numeric format
        df[price_column] = pd.to_numeric(df[price_column])

        # Aggregate daily mean prices
        daily_summary = df.resample("D").mean()

        # Drop rows where price_column is NaN
        daily_summary.dropna(subset=[price_column], inplace=True)

        logger.info(f"Successfully aggregated raw prices to daily averages.")
        return daily_summary.reset_index()

    except Exception as e:
        logger.error(f"Error aggregating to day-based prices: {e}")
        raise
