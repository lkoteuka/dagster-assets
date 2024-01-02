from dagster import load_assets_from_current_module, AutoMaterializePolicy

from dagster_assets.assets.lookups.payment_type_lookup import payment_type_lookup_asset
from dagster_assets.config import LOOKUP_GROUP

lookup_assets = load_assets_from_current_module(
    auto_materialize_policy=AutoMaterializePolicy.eager(),
    group_name=LOOKUP_GROUP,
)
