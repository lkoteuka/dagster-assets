from dagster import load_assets_from_current_module, AutoMaterializePolicy

from dagster_assets.assets.daily.payment_type_revenue_daily import payment_type_revenue_daily_asset
from dagster_assets.assets.daily.company_revenue_daily import company_revenue_daily_asset
from dagster_assets.config import DAILY_GROUP

daily_assets = load_assets_from_current_module(
    auto_materialize_policy=AutoMaterializePolicy.eager(),
    group_name=DAILY_GROUP,
)