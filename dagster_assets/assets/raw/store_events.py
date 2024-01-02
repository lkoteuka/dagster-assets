from dagster import AssetKey, SourceAsset, DailyPartitionsDefinition

from dagster_assets.assets.utils import observe_raw_assets_partitions_fn
from dagster_assets.config import RAW_GROUP, ASSET_DAILY_PARTITION_START_DATE, OBSERVE_INTERVAL_MINUTES, \
    ASSET_DAILY_PARTITION_END_DATE

OBJECT_NAME = "store_events"

"""
## Schema

| company_id | store_id | payment_code | revenue |
|------------|----------|--------------|---------|
...
"""

store_events_us_asset = SourceAsset(
    key=AssetKey(["raw", "us", OBJECT_NAME]),
    group_name=RAW_GROUP,
    partitions_def=DailyPartitionsDefinition(start_date=ASSET_DAILY_PARTITION_START_DATE,
                                             end_date=ASSET_DAILY_PARTITION_END_DATE),
    observe_fn=observe_raw_assets_partitions_fn,
    auto_observe_interval_minutes=OBSERVE_INTERVAL_MINUTES,
)

store_events_eu_asset = SourceAsset(
    key=AssetKey(["raw", "eu", OBJECT_NAME]),
    group_name=RAW_GROUP,
    partitions_def=DailyPartitionsDefinition(start_date=ASSET_DAILY_PARTITION_START_DATE,
                                             end_date=ASSET_DAILY_PARTITION_END_DATE),
    observe_fn=observe_raw_assets_partitions_fn,
    auto_observe_interval_minutes=OBSERVE_INTERVAL_MINUTES,
)
