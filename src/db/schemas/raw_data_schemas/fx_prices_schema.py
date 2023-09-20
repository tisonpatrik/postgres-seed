from typing import Dict

from src.db.schemas.base_config_schema import BaseConfigSchema


class FxPricesSchema(BaseConfigSchema):
    @property
    def column_mapping(self) -> Dict[str, str]:
        return {"DATETIME": "unix_date_time", "PRICE": "price"}

    @property
    def sql_command(self) -> str:
        return """
                CREATE TABLE fx_prices (
                        unix_date_time INTEGER,
                        symbol VARCHAR(50),
                        price FLOAT,
                        PRIMARY KEY (unix_date_time, symbol)
                    )
                """

    @property
    def table_name(self) -> str:
        return "fx_prices"

    @property
    def origin_csv_file_path(self) -> str:
        return "/path/in/container/fx_prices_csv/"
