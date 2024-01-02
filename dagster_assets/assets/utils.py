import glob
from os import path

from dagster import OpExecutionContext, DataVersion, DataVersionsByPartition, asset_check

from dagster_assets.config import DATA_PATH


def observe_raw_assets_partitions_fn(context: OpExecutionContext) -> DataVersion:
    """
    Return  DataVersion's for all ready partitions
    :param context:
    :return: DataVersion
    """
    asset_key = [s for s in context.op.name.split("__")]
    source_path = path.join(DATA_PATH, "raw", asset_key[1], asset_key[2])

    data_partitions = glob.glob(f"{source_path}/*.csv")

    if len(data_partitions) > 0:
        partitions = {date: date for date in data_partitions}
        context.log.info(f"Founded {len(data_partitions)} partitions.")
        return DataVersionsByPartition(partitions)
    else:
        context.log.warning(f"Empty data for SourceAsset with key: {asset_key}")
        return DataVersionsByPartition({})
