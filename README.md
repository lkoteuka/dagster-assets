# dagster_assets

This is a Dagster-assets project for demonstrating main advantages of Dagster software-defined assets. 

## Getting started

Build a Docker image in root of the project:

```bash
docker build -t dagster-assets .
```

Then, start the Docker container with exposed port and mounted volume (you need ± 1Mb of free space for storing auto-generated data):

```bash
docker run -p 3000:3000 --rm -it -v ${PWD}/data/:/user_code/data/ dagster-assets
```

Open http://localhost:3000 with your browser to see Dagster UI.

Generate a raw data and lookup table with job named 'create_data_job' with default config from launchpad.

Next step go to the "Assets" page, then to "View global asset lineage":

Click "Observe sources", to observe our "raw" data and check daily partitioned data for each of SourceAsset.

You can check that raw data was created correctly, if you see all four partitions (from 2024-01-01 to 2023-01-04) in asset catalog with expanded info about each of asset.

Materialize dependent Assets simultaneously or separately for the desired dates. After this, you can view aggregated information in the “plots” Dagster UI page or full tables for analytics in the corresponding directory (by default ./data)