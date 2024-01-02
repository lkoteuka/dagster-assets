from dagster import with_resources

from dagster_assets.assets.daily import daily_assets
from dagster_assets.assets.lookups import lookup_assets
from dagster_assets.assets.raw import raw_assets
from dagster_assets.config import DATA_PATH
from dagster_assets.io_manager.daily_io_manager import daily_io_manager

COMMON_ASSETS_RESOURCE = {
    "io_manager": daily_io_manager,
}

COMMON_ASSETS_RESOURCE_CONFIG = {
    "io_manager": {
        "config": {
            # not required, because has default_value
            "data_path": DATA_PATH
        }
    }
}

assets_definition = with_resources(
    definitions=[
        *lookup_assets,
        *daily_assets,
        *raw_assets,
    ],
    resource_defs=COMMON_ASSETS_RESOURCE,
    resource_config_by_key=COMMON_ASSETS_RESOURCE_CONFIG,
)
