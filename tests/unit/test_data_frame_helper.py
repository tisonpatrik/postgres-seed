import pandas as pd
import pytest

from src.data_processing.data_frame_helper import (
    add_symbol_by_file_name,
    aggregate_to_day_based_prices,
    convert_column_to_datetime,
    convert_datetime_to_unixtime,
    fill_empty_values,
    rename_columns,
)
from src.data_processing.errors import (
    ColumnRenameError,
    DataAggregationError,
    DateTimeConversionError,
    EmptyValueFillError,
    InvalidDatetimeColumnError,
    SymbolAdditionError,
)


# Mock logger for testing
class MockLogger:
    def error(self, *args):
        pass


logger = MockLogger()


def test_rename_columns_success(mock_dataframe):
    new_column_names = {"DATETIME": "unix_date_time", "price": "price"}
    renamed_df = rename_columns(mock_dataframe, new_column_names)
    assert list(renamed_df.columns) == ["unix_date_time", "price"]


def test_rename_columns_fail(mock_dataframe):
    new_column_names = {"wrong_column": "unix_date_time", "price": "price"}
    with pytest.raises(ColumnRenameError):
        rename_columns(mock_dataframe, new_column_names)


def test_fill_empty_values_success(mock_dataframe_with_empty_values):
    fill_value = 0
    filled_df = fill_empty_values(mock_dataframe_with_empty_values, fill_value)
    assert (
        filled_df.isna().sum().sum() == 0
    )  # Check that there are no NaN values in the DataFrame


def test_fill_empty_values_fail(mock_dataframe_with_empty_values):
    fill_value = {"wrong_column": 0}
    with pytest.raises(EmptyValueFillError):
        fill_empty_values(mock_dataframe_with_empty_values, fill_value)


def test_add_symbol_by_file_name(mock_dataframe_for_symbol):
    symbol = "AAPL"
    df_with_symbol = add_symbol_by_file_name(mock_dataframe_for_symbol, symbol)
    assert "symbol" in df_with_symbol.columns
    assert all(df_with_symbol["symbol"] == symbol)


def test_add_symbol_by_file_name_fail():
    with pytest.raises(SymbolAdditionError):
        add_symbol_by_file_name(None, "AAPL")  # Passing None instead of a DataFrame


def test_convert_datetime_to_unixtime(mock_dataframe_for_datetime):
    df_unix_time = convert_datetime_to_unixtime(mock_dataframe_for_datetime)
    assert "unix_date_time" in df_unix_time.columns
    assert df_unix_time["unix_date_time"].dtype == "int64"


def test_convert_datetime_to_unixtime_fail(
    mock_dataframe_for_symbol,
):  # Reusing the first fixture as a wrong input
    with pytest.raises(DateTimeConversionError):
        convert_datetime_to_unixtime(mock_dataframe_for_symbol)


# Test for successful data aggregation
def test_aggregate_to_day_based_prices_success(
    mock_dataframe_for_aggregation_success, expected_dataframe_for_aggregation_success
):
    result = aggregate_to_day_based_prices(mock_dataframe_for_aggregation_success)

    # Check if the DataFrame is as expected
    pd.testing.assert_frame_equal(
        result, expected_dataframe_for_aggregation_success, check_dtype=False
    )

    # Check if there are no empty values in 'price'
    assert result["price"].isna().sum() == 0

    # Check if 'price' is rounded to 1 decimal place
    assert all(result["price"].apply(lambda x: x == round(x, 1)))


# Test for failed data aggregation
def test_aggregate_to_day_based_prices_fail(mock_dataframe_for_aggregation_fail):
    with pytest.raises(DataAggregationError):
        aggregate_to_day_based_prices(mock_dataframe_for_aggregation_fail)


# Test for successful datetime conversion
def test_convert_column_to_datetime_success(mock_dataframe_for_datetime_success):
    result = convert_column_to_datetime(
        mock_dataframe_for_datetime_success, "datetime_column"
    )
    assert result["datetime_column"].dtype == "datetime64[ns]"


# Test for failed datetime conversion
def test_convert_column_to_datetime_fail(mock_dataframe_for_datetime_fail):
    with pytest.raises(InvalidDatetimeColumnError):
        convert_column_to_datetime(mock_dataframe_for_datetime_fail, "datetime_column")
