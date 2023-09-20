from src.db.schemas.config_schemas.instrument_config_schema import (
    InstrumentConfigSchema,
)
from src.db.schemas.config_schemas.instrument_metadata_schema import (
    InstrumentMetadataSchema,
)
from src.db.schemas.config_schemas.roll_config_schema import RollConfigSchema
from src.db.schemas.config_schemas.spread_cost_schema import SpreadCostSchema
from src.db.schemas.raw_data_schemas.adjusted_prices_schema import AdjustedPricesSchema
from src.db.schemas.raw_data_schemas.fx_prices_schema import FxPricesSchema
from src.db.schemas.raw_data_schemas.multiple_prices_schema import MultiplePricesSchema
from src.db.schemas.raw_data_schemas.roll_calendars_schema import RollCalendarsSchema


def get_schemas():
    return [
        InstrumentConfigSchema(),
        InstrumentMetadataSchema(),
        RollConfigSchema(),
        SpreadCostSchema(),
        AdjustedPricesSchema(),
        FxPricesSchema(),
        MultiplePricesSchema(),
        RollCalendarsSchema(),
    ]


def get_configs_schemas():
    return [
        InstrumentConfigSchema(),
        InstrumentMetadataSchema(),
        RollConfigSchema(),
        SpreadCostSchema(),
    ]


def get_raw_data_schemas():
    return [
        AdjustedPricesSchema(),
        FxPricesSchema(),
        MultiplePricesSchema(),
        RollCalendarsSchema(),
    ]
