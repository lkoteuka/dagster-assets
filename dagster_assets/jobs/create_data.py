from dagster import job

from dagster_assets.config import ASSET_DAILY_PARTITION_START_DATE, ASSET_DAILY_PARTITION_END_DATE, DATA_PATH
from dagster_assets.ops.create_data import create_raw_data_op, create_lookup_data_op

CREATE_RAW_DATA_JOB_CONFIG = {
    "ops": {
        "create_raw_data_op": {
            "config": {
                "from_date": ASSET_DAILY_PARTITION_START_DATE,
                "to_date": ASSET_DAILY_PARTITION_END_DATE,
                "data_path": DATA_PATH,
                "data_centers": ["us", "eu"],
            }
        },
        "create_lookup_data_op": {
            "config": {
                "data_path": DATA_PATH,
            }
        }
    }
}


@job(config=CREATE_RAW_DATA_JOB_CONFIG)
def create_data_job():
    create_raw_data_op()
    create_lookup_data_op()
