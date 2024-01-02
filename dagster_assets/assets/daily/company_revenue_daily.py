import pandas as pd
import dagster as dg
from dagster import DailyPartitionsDefinition, AssetKey, Output

from dagster_assets.config import ASSET_DAILY_PARTITION_START_DATE, ASSET_DAILY_PARTITION_END_DATE

KEY_COLUMNS = ["company_id", "store_id", "payment_code"]

"""
## Schema

| date | company_id | store_id | payment_code | sum(revenue) as revenue | count(*) as event_count |
|------|------------|----------|--------------|-------------------------|-------------------------|
...
"""


@dg.asset(
    key=AssetKey(["daily", "company_revenue_daily"]),
    ins={
        "store_events_eu_raw": dg.AssetIn(
            key=dg.AssetKey(["raw", "eu", "store_events"]),
            input_manager_key="io_manager",
        ),
        "store_events_us_raw": dg.AssetIn(
            key=dg.AssetKey(["raw", "us", "store_events"]),
            input_manager_key="io_manager",
        ),
    },
    partitions_def=DailyPartitionsDefinition(start_date=ASSET_DAILY_PARTITION_START_DATE,
                                             end_date=ASSET_DAILY_PARTITION_END_DATE),
    io_manager_key="io_manager",
)
def company_revenue_daily_asset(
        context,
        store_events_eu_raw: pd.DataFrame,
        store_events_us_raw: pd.DataFrame,
):

    result_df = pd.concat([store_events_eu_raw, store_events_us_raw])

    result_df["event_count"] = 1
    result_df = result_df.groupby(KEY_COLUMNS, as_index=False)[["revenue", "event_count"]].sum()

    result_df["date"] = context.asset_partition_key_for_output()

    # save num_rows to metadata
    return Output(result_df, metadata={"num_rows": result_df.shape[0], "revenue_total": result_df["revenue"].sum()})
