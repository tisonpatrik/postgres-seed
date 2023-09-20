from unittest.mock import AsyncMock, MagicMock, patch

import pandas as pd
import pytest

from src.db.repositories.data_loader import DataLoader

# Mock data to simulate fetched rows from the database
mock_rows = [{"id": 1, "name": "test_name_1"}, {"id": 2, "name": "test_name_2"}]


@pytest.mark.asyncio
async def test_fetch_data_as_dataframe_async():
    # Setup
    sql_template = "SELECT * FROM test_table WHERE id = :id"
    parameters = {"id": 1}

    with patch.object(
        DataLoader, "_create_connection_pool", new_callable=AsyncMock
    ) as mock_pool, patch.object(
        DataLoader, "_execute_sql", new_callable=AsyncMock, return_value=mock_rows
    ), patch.object(
        DataLoader, "_convert_to_dataframe", return_value=pd.DataFrame(mock_rows)
    ):
        loader = DataLoader("test_db_url")
        df = await loader.fetch_data_as_dataframe_async(sql_template, parameters)

    assert not df.empty
    assert df.iloc[0]["name"] == "test_name_1"
    mock_pool.assert_called_once()


@pytest.mark.asyncio
async def test_create_connection_pool():
    with patch("asyncpg.create_pool", new_callable=AsyncMock) as mock_create_pool:
        loader = DataLoader("test_db_url")
        await loader._create_connection_pool()
        mock_create_pool.assert_called_once_with(dsn="test_db_url")
