from os import path, rmdir, pardir, walk
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

    data_dir_paths = [path.join(dirpath, dir_) for (dirpath, dirnames, filenames) in walk(data_path) for dir_ in dirnames]

    for dir_path in data_dir_paths:
        if path.exists(dir_path):
            shutil.rmtree(dir_path)
        else:
            print(f"Can't remove path: '{dir_path}'")

    return Nothing()
