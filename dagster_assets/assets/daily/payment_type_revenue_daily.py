import pandas as pd
import dagster as dg
from dagster import DailyPartitionsDefinition, AssetKey, Output

from dagster_assets.config import ASSET_DAILY_PARTITION_START_DATE, ASSET_DAILY_PARTITION_END_DATE

"""
Table: 'payment_type_revenue_daily'
Schema:

| date | payment_code | sum(revenue) as revenue | sum(event_count) as event_count |
|------|--------------|-------------------------|---------------------------------|
...
"""


@dg.asset(
    key=AssetKey(["daily", "payment_type_revenue_daily"]),
    ins={
        "company_revenue_daily": dg.AssetIn(
            key=dg.AssetKey(["daily", "company_revenue_daily"]),
            input_manager_key="io_manager",
        ),
        "payment_code_type": dg.AssetIn(
            key=AssetKey(["lookup", "payment_code_type"]),
            input_manager_key="io_manager",
        ),
    },
    partitions_def=DailyPartitionsDefinition(start_date=ASSET_DAILY_PARTITION_START_DATE,
                                             end_date=ASSET_DAILY_PARTITION_END_DATE),
    io_manager_key="io_manager",
)
def payment_type_revenue_daily_asset(
        context,
        company_revenue_daily: pd.DataFrame,
        payment_code_type: pd.DataFrame,
):
    payment_type_revenue_daily = company_revenue_daily \
        .groupby(["date", "payment_code"], as_index=False)[["revenue", "event_count"]].sum()

    payment_type_revenue_daily = payment_type_revenue_daily.merge(payment_code_type,
                                                                  on=["payment_code"],
                                                                  how="left").reset_index()

    context.log.info(payment_type_revenue_daily.head())
    context.log.info(payment_type_revenue_daily.columns)

    payment_type_revenue_daily = payment_type_revenue_daily[["date",
                                                             "payment_type",
                                                             "revenue",
                                                             "event_count"]]

    # save event_count to metadata
    return Output(payment_type_revenue_daily,
                  metadata={"event_count": int(payment_type_revenue_daily["event_count"].sum())})
