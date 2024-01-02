from os import path, rmdir, pardir
import shutil

from dagster import op, Field, OpExecutionContext, Nothing


@op(
    config_schema={
        "data_path": Field(str, is_required=True),
    },
)
def delete_data_op(context: OpExecutionContext):
    data_path = path.join(path.join(path.join(path.dirname(__file__), pardir), pardir),
                          context.op_config.get("data_path"))
    if path.exists(data_path):
        shutil.rmtree(data_path)
    else:
        print(f"Can't remove path: '{data_path}'")

    return Nothing()
