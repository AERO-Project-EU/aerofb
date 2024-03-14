import json
import os
import os.path

from minio import Minio


ACCESS_KEY = "minioroot"
SECRET_KEY = "minioroot"

TMP = "/tmp"


def function_handler(function_input):
    # Parse function input
    payload = json.loads(bytes(function_input["payload"]).decode("utf-8"))
    minio_address = payload["minio_address"]
    bucket_name = payload["bucket_name"]
    file_name = payload["file_name"]
    file_path = os.path.join(TMP, file_name)

    # Download the input JSON file from MinIO
    minio_client = Minio(
        minio_address,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False,
    )
    minio_client.fget_object(bucket_name, file_name, file_path)

    # Process input
    with open(file_path) as fin:
        data = fin.read()
    json_data = json.loads(data)
    _ = json.dumps(json_data, indent=4)
