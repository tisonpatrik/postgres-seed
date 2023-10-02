"""
CSV Helper module.

This module provides utility functions for loading and saving data to CSV files. 
It contains functions `load_csv` to load data from a CSV file into a DataFrame and `save_to_csv` 
to save a DataFrame to a CSV file. A private utility function `_get_full_path` is used internally 
to get the full path to a file by combining the base and provided paths.
"""

import logging

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_csv(path: str, base_path: str = "") -> pd.DataFrame:
    """Load CSV file from the given path.
    Args:
        path (str): Path to the CSV file.
        base_path (str): Base path for the CSV file.

    Returns:
        pd.DataFrame: Loaded dataframe.
    """
    full_path = _get_full_path(base_path, path)
    try:
        logger.info("Loading CSV file from %s", full_path)
        return pd.read_csv(full_path)
    except Exception as error:
        logger.error("Error loading CSV file from %s: %s", full_path, error)
        raise


def save_to_csv(data_frame: pd.DataFrame, path: str, base_path: str = ""):
    """Save dataframe to the given CSV path.

    Args:
        data_frame (pd.DataFrame): Dataframe to save.
        path (str): Path to save the CSV file to.
        base_path (str): Base path for the CSV file.
    """
    full_path = _get_full_path(base_path, path)
    try:
        data_frame.to_csv(full_path, index=False)
        logger.info("Data saved to %s", full_path)
    except Exception as error:
        logger.error("Error saving data to %s: %s", full_path, error)
        raise


def _get_full_path(base_path: str, path: str) -> str:
    """Get the full path to a file, combining base and provided path."""
    return base_path + "/" + path
