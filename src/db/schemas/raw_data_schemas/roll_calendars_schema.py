from typing import Dict

from src.db.schemas.base_config_schema import BaseConfigSchema


class RollCalendarsSchema(BaseConfigSchema):
    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            "DATE_TIME": "unix_date_time",
            "current_contract": "current_contract",
            "next_contract": "next_contract",
            "carry_contract": "carry_contract",
        }

    @property
    def sql_command(self) -> str:
        return """
                CREATE TABLE roll_calendars (
                        unix_date_time INTEGER,
                        symbol VARCHAR(50),
                        current_contract INTEGER,
                        next_contract INTEGER,
                        carry_contract INTEGER,
                        PRIMARY KEY (unix_date_time, symbol)
                    )
                """

    @property
    def table_name(self) -> str:
        return "roll_calendars"

    @property
    def origin_csv_file_path(self) -> str:
        return "/path/in/container/roll_calendars_csv/"
