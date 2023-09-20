from src.db.schemas.base_config_schema import BaseConfigSchema
from typing import Dict

class MultiplePricesSchema(BaseConfigSchema):

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            'DATETIME': 'unix_date_time',
            'CARRY': 'carry', 
            'CARRY_CONTRACT': 'carry_contract', 
            'PRICE': 'price', 
            'PRICE_CONTRACT': 'price_contract',
            'FORWARD': 'forward',
            'FORWARD_CONTRACT': 'forward_contract'
            }

    @property
    def sql_command(self) -> str:
        return """
            CREATE TABLE multiple_prices (
                    unix_date_time INTEGER,
                    symbol VARCHAR(50),
                    carry FLOAT, 
                    carry_contract INTEGER, 
                    price FLOAT, 
                    price_contract INTEGER, 
                    forward FLOAT, 
                    forward_contract INTEGER,
                    adjusted_price FLOAT,  -- Added the missing comma here
                    PRIMARY KEY (unix_date_time, symbol)
                )
            """
    
    @property
    def table_name(self) -> str:
        return "multiple_prices"
    
    @property
    def origin_csv_file_path(self) -> str:
        return "/path/in/container/multiple_prices_csv/"