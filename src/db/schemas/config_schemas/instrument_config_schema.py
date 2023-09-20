from src.db.schemas.base_config_schema import BaseConfigSchema
from typing import Dict

class InstrumentConfigSchema(BaseConfigSchema):

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            'Instrument': 'symbol', 
            'Description': 'description', 
            'Pointsize': 'pointsize', 
            'Currency': 'currency', 
            'AssetClass': 'asset_class', 
            'PerBlock': 'per_block', 
            'Percentage': 'percentage', 
            'PerTrade': 'per_trade', 
            'Region': 'region'
            }

    @property
    def sql_command(self) -> str:
        return """
                CREATE TABLE instrument_config (
                        symbol VARCHAR(50) PRIMARY KEY, 
                        description TEXT, 
                        pointsize FLOAT, 
                        currency VARCHAR(10), 
                        asset_class VARCHAR(50), 
                        per_block FLOAT, 
                        percentage FLOAT, 
                        per_trade INTEGER, 
                        region VARCHAR(50)
                    )
                """
    
    @property
    def table_name(self) -> str:
        return "instrument_config"
    
    @property
    def origin_csv_file_path(self) -> str:
        return "/path/in/container/csvconfig/instrumentconfig.csv"