from dagster import repository

from dagster_assets.assets.assets_definition import assets_definition
from dagster_assets.jobs.create_data import create_data_job
from dagster_assets.jobs.delete_data import delete_data_job


@repository
def dagster_assets():
    """
    The repository definition for this pipeline Dagster repository.

    For hints on building your Dagster repository, see our documentation overview on Repositories:
    https://docs.dagster.io/overview/repositories-workspaces/repositories
    """

    assets = [
        *assets_definition,
    ]

    jobs = [
        create_data_job,
        delete_data_job,
    ]

    return assets + jobs
