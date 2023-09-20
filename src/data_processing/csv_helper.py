import pandas as pd
import logging
import os
from typing import List

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
        logger.info(f"Loading CSV file from {full_path}")
        return pd.read_csv(full_path)
    except Exception as e:
        logger.error(f"Error loading CSV file from {full_path}: {e}")
        raise

def save_to_csv(df: pd.DataFrame, path: str, base_path: str = ""):
    """Save dataframe to the given CSV path.

    Args:
        df (pd.DataFrame): Dataframe to save.
        path (str): Path to save the CSV file to.
        base_path (str): Base path for the CSV file.
    """
    full_path = _get_full_path(base_path, path)
    try:
        df.to_csv(full_path, index=False)
        logger.info(f"Data saved to {full_path}")
    except Exception as e:
        logger.error(f"Error saving data to {full_path}: {e}")
        raise

def _get_full_path(base_path: str, path: str) -> str:
    """Get the full path to a file, combining base and provided path."""
    return base_path + "/" + path