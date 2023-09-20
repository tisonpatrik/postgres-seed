from src.db.schemas.base_config_schema import BaseConfigSchema
from typing import Dict

class InstrumentMetadataSchema(BaseConfigSchema):

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            'Instrument': 'symbol',
            'AssetClass': 'asset_class',
            'SubClass': 'sub_class',
            'SubSubClass':'sub_sub_class',
            'Style': 'style',
            'Country': 'country',
            'Duration': 'duration',
            'Description': 'description'
            }

    @property
    def sql_command(self) -> str:
        return """
                CREATE TABLE instrument_metadata (
                    symbol VARCHAR(50) PRIMARY KEY,
                    asset_class VARCHAR(50),
                    sub_class VARCHAR(50),
                    sub_sub_class VARCHAR(50),
                    description VARCHAR(100)
                )
                """
    
    @property
    def table_name(self) -> str:
        return "instrument_metadata"
    
    @property
    def origin_csv_file_path(self) -> str:
        return "/path/in/container/csvconfig/moreinstrumentinfo.csv"