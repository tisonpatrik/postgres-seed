from src.db.schemas.base_config_schema import BaseConfigSchema
from typing import Dict

class RollConfigSchema(BaseConfigSchema):

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
                'Instrument': 'symbol',
                'HoldRollCycle': 'hold_roll_cycle',
                'RollOffsetDays': 'roll_offset_days',
                'CarryOffset': 'carry_offset',
                'PricedRollCycle': 'priced_roll_cycle',
                'ExpiryOffset': 'expiry_offset'
                }


    @property
    def sql_command(self) -> str:
        return """
                CREATE TABLE roll_config (
                    symbol VARCHAR(50) PRIMARY KEY,
                    hold_roll_cycle VARCHAR(50),
                    roll_offset_days INTEGER,
                    carry_offset INTEGER,
                    priced_roll_cycle VARCHAR(50),
                    expiry_offset INTEGER
                )
                """
    
    @property
    def table_name(self) -> str:
        return "roll_config"
    
    @property
    def origin_csv_file_path(self) -> str:
        return "/path/in/container/csvconfig/rollconfig.csv"