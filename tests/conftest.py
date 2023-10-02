# conftest.py

import pandas as pd
import pytest


# Fixture to mock a DataFrame similar to AEX.csv
@pytest.fixture
def mock_dataframe():
    data = {
        "DATETIME": ["2009-08-18 23:00:00", "2009-08-19 23:00:00"],
        "price": [89.57, 89.27],
    }
    return pd.DataFrame(data)


# Fixture to mock a DataFrame with empty values
@pytest.fixture
def mock_dataframe_with_empty_values():
    data = {"column1": [1, 2, None, 4], "column2": [None, 2, 3, 4]}
    return pd.DataFrame(data)


# Fixture to mock a DataFrame suitable for add_symbol_by_file_name
@pytest.fixture
def mock_dataframe_for_symbol():
    data = {"column1": [1, 2, 3], "column2": [4, 5, 6]}
    return pd.DataFrame(data)


# Fixture to mock a DataFrame suitable for convert_datetime_to_unixtime
@pytest.fixture
def mock_dataframe_for_datetime():
    data = {"unix_date_time": ["2022-01-01 00:00:00", "2022-01-02 00:00:00"]}
    return pd.DataFrame(data)


# Mock DataFrame for successful aggregation
@pytest.fixture
def mock_dataframe_for_aggregation_success():
    data = {
        "unix_date_time": [
            "2022-01-01 01:00:00",
            "2022-01-01 02:00:00",
            "2022-01-02 01:00:00",
        ],
        "price": [1.0, 2.0, 3.0],
    }
    return pd.DataFrame(data)


@pytest.fixture
def expected_dataframe_for_aggregation_success():
    data = {
        "unix_date_time": pd.to_datetime(
            ["2022-01-01", "2022-01-02"]
        ),  # Convert to datetime
        "price": [1.5, 3.0],
    }
    return pd.DataFrame(data)


# Mock DataFrame for failed aggregation (non-numeric 'price')
@pytest.fixture
def mock_dataframe_for_aggregation_fail():
    data = {
        "unix_date_time": ["2022-01-01 01:00:00", "2022-01-01 02:00:00"],
        "price": ["not_a_number", "another_non_number"],
    }
    return pd.DataFrame(data)


# Mock DataFrame for successful datetime conversion
@pytest.fixture
def mock_dataframe_for_datetime_success():
    data = {"datetime_column": ["2022-01-01", "2022-01-02"]}
    return pd.DataFrame(data)


# Mock DataFrame for failed datetime conversion
@pytest.fixture
def mock_dataframe_for_datetime_fail():
    data = {"datetime_column": ["not_a_datetime", "another_not_datetime"]}
    return pd.DataFrame(data)
