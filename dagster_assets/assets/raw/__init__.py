from dagster import load_assets_from_current_module, AutoMaterializePolicy

from dagster_assets.assets.raw.store_events import store_events_eu_asset, store_events_us_asset

raw_assets = load_assets_from_current_module(
    auto_materialize_policy=AutoMaterializePolicy.eager(),
)
