from datetime import datetime, timedelta
from os import path, makedirs, pardir

import numpy as np
import pandas as pd
from dagster import Array, op, Field, OpExecutionContext, Nothing

from dagster_assets.assets.raw.store_events import OBJECT_NAME
from dagster_assets.config import DATE_FORMAT


@op(
    config_schema={
        "from_date": Field(str, is_required=True),
        "to_date": Field(str, is_required=True),
        "data_path": Field(str, is_required=True),
        "data_centers": Field(Array(str), is_required=True),
    },
)
def create_raw_data_op(context: OpExecutionContext):
    def generate_raw_dataframe(num_rows=20):
        """
        Generate raw data by schema:
        | company_id | store_id | payment_code | revenue |
        |------------|----------|--------------|---------|
        :param num_rows:
        :return: pd.DataFrame
        """
        raw_df = pd.DataFrame(np.random.default_rng().integers(1, 4, size=(num_rows, 4)),
                              columns=["company_id", "store_id", "payment_code", "revenue"])
        raw_df["revenue"] = raw_df["revenue"].astype("float")
        return raw_df

    from_date = datetime.strptime(context.op_config["from_date"], DATE_FORMAT)
    to_date = datetime.strptime(context.op_config["to_date"], DATE_FORMAT)

    data_path = path.join(path.join(path.join(path.dirname(__file__), pardir), pardir), context.op_config["data_path"])
    data_centers = context.op_config["data_centers"]

    if from_date > to_date:
        raise ValueError(f"to_date must be greater than from_date.")

    while from_date < to_date:
        context.log.info(f"Create raw data for date: '{from_date.strftime(DATE_FORMAT)}'")
        for data_center in data_centers:
            raw_dc_path = path.join(data_path, "raw", data_center, OBJECT_NAME)

            if not path.exists(raw_dc_path):
                makedirs(raw_dc_path)

            raw_dc_df = generate_raw_dataframe()
            raw_dc_df.to_csv(f"{path.join(raw_dc_path, from_date.strftime(DATE_FORMAT))}.csv",
                             index=False,
                             header=True)
        from_date = from_date + timedelta(days=1)

    return Nothing()


@op(
    config_schema={
        "data_path": Field(str, is_required=True),
    },
)
def create_lookup_data_op(context: OpExecutionContext):
    lookup_path = path.join(path.join(path.join(path.dirname(__file__), pardir), pardir),
                            context.op_config["data_path"],
                            "lookup")

    if not path.exists(lookup_path):
        makedirs(lookup_path)

    payment_type_lookup_df = pd.DataFrame({'payment_code': [1, 2, 3],
                                           'payment_type': ["cash", "debit_card", "credit_card"]})

    payment_type_path = path.join(lookup_path, "payment_code_type")
    payment_type_lookup_df.to_csv(f"{payment_type_path}.csv", index=False, header=True)

    return Nothing()
