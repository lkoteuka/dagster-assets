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

TODO generate a raw data and lookup with job named 'create_data_job' with default config from launchpad.

TODO observe SourceAssets from Assset -> asset lineage 

TODO Materialize daily assets by partitions