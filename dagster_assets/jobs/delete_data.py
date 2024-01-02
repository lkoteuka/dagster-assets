from dagster import job

from dagster_assets.config import ASSET_DAILY_PARTITION_START_DATE, ASSET_DAILY_PARTITION_END_DATE, DATA_PATH
from dagster_assets.ops.create_data import create_raw_data_op, create_lookup_data_op
from dagster_assets.ops.delete_data import delete_data_op

DELETE_DATA_JOB_CONFIG = {
    "ops": {
        "delete_data_op": {
            "config": {
                "data_path": DATA_PATH,
            }
        }
    }
}


@job(config=DELETE_DATA_JOB_CONFIG)
def delete_data_job():
    delete_data_op()
