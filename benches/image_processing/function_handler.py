from inspect import getmembers, isfunction
import json
import os
import os.path

from PIL import Image
from minio import Minio

import ops


ACCESS_KEY = "minioroot"
SECRET_KEY = "minioroot"

TMP = "/tmp"


# List of names of all functions defined in module `ops`
OPS = list(map(lambda t: t[0], getmembers(ops, isfunction)))


def image_processing(file_name: str, image_path: str, req_ops: list[str]):
    path_list = []
    with Image.open(image_path) as image:
        for op in req_ops:
            path_list += eval(f"ops.{op}(image, file_name)")
    return path_list


def function_handler(function_input):
    # Parse function input
    #payload = json.loads(function_input["payload"].decode("utf-8"))
    payload = json.loads(bytes(function_input["payload"]).decode("utf-8"))
    minio_address = payload["minio_address"]
    bucket_name = payload["bucket_name"]
    img_name = payload["img_name"]
    try:
        req_ops = list(map(str.lower, payload["ops"].split("-")))
        for op in req_ops:
            if op not in OPS:
                raise ValueError(f"invalid op '{op}'; choose among {OPS}")
    except KeyError:
        # if no payload["ops"] specified, be backwards compat with 0.0.2-dev
        req_ops = ["rotate"]  # XXX or `req_ops = OPS` to apply them all?

    # Download the input image from MinIO
    img_path = os.path.join(TMP, img_name)
    minio_client = Minio(
        minio_address,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False,
    )
    minio_client.fget_object(bucket_name, img_name, img_path)

    # Process input
    img_paths = image_processing(img_name, img_path, req_ops)

    # Upload all output images to MinIO
    # for upload_path in img_paths:
    #     minio_client.fput_object(
    #         bucket_name, upload_path.split("/")[2], upload_path
    #     )
    for img_p in img_paths:
        os.remove(img_p)

    return {"image_paths": img_paths}
