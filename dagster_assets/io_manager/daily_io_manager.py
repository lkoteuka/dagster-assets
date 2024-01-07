from os import path, pardir, makedirs

import pandas as pd
from dagster import (
    Field,
    IOManager,
    InputContext,
    OutputContext,
    io_manager,
)

from dagster_assets.config import DATA_PATH


class DailyIOManager(IOManager):
    source_types = ["raw", "lookup", "daily"]

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        """Write data"""

        partition_date = ""
        if context.has_partition_key:
            partition_date = context.asset_partition_key

        asset_key: list[str] = context.asset_key.path
        table_path = path.join(path.join(path.join(path.dirname(__file__), pardir), pardir),
                               context.resource_config.get("data_path"),
                               *asset_key)

        if not path.exists(table_path):
            makedirs(table_path)

        if asset_key[0] == "raw":
            # We can't overwrite raw data, so just pass this step
            pass
        elif asset_key[0] == "daily":
            table_partition_path = path.join(table_path, partition_date)
            obj.to_csv(f"{table_partition_path}.csv", index=False)
        elif asset_key[0] == "lookup":
            obj.to_csv(f"{table_path}.csv", index=False)
        else:
            raise ValueError(f"Can't handle output for source name: '{asset_key[0]}'")

    def load_input(self, context: InputContext):
        """Read data"""

        partition_date = ""
        if context.has_partition_key:
            partition_date = context.partition_key

        asset_key: list[str] = context.asset_key.path
        context.log.info(f"Try load `{asset_key}`")
        table_path = path.join(path.join(path.join(path.dirname(__file__), pardir), pardir),
                               context.resource_config.get("data_path"),
                               *asset_key)
        context.log.info(f"Try load `{asset_key}`")

        if asset_key[0] in ["raw", "daily"]:
            # Separate file for each date partition
            table_path = path.join(table_path, partition_date)
            context.log.info(f"Read `{table_path}.csv`")
            return pd.read_csv(f"{table_path}.csv")
        elif asset_key[0] == "lookup":
            # Only one file, without partitions
            context.log.info(f"Read `{table_path}.csv`")
            return pd.read_csv(f"{table_path}.csv")
        else:
            raise ValueError(f"Can't handle input for source type: '{asset_key[0]}'")


@io_manager(
    config_schema={
        "data_path": Field(
            str,
            is_required=False,
            default_value=DATA_PATH,
        ),
    },
)
def daily_io_manager():
    return DailyIOManager()
