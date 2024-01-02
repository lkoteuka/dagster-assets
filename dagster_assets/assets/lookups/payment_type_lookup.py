from dagster import AssetKey, SourceAsset


"""
## Schema

| payment_code | payment_type |
|--------------|--------------|
...
"""


payment_type_lookup_asset = SourceAsset(
    key=AssetKey(["lookup", "payment_code_type"]),
)
