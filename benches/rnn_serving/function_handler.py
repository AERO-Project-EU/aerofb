import json
import os.path
import pickle

import torch
from minio import Minio

import rnn


torch.set_num_threads(1)

ACCESS_KEY = "minioroot"
SECRET_KEY = "minioroot"

TMP = "/tmp"


def function_handler(function_input):
    # Parse function input
    #payload = json.loads(function_input["payload"].decode("utf-8"))
    payload = json.loads(bytes(function_input["payload"]).decode("utf-8"))
    language = payload["language"]
    start_letters = payload["start_letters"]
    minio_address = payload["minio_address"]
    bucket_name = payload["bucket_name"]
    model_parameter_object_key = payload[
        "model_parameter_object_key"
    ]  # e.g.: rnn_params.pkl
    model_object_key = payload["model_object_key"]  # e.g.: rnn_model.pth

    # Initialize the MinIO client
    minio_client = Minio(
        minio_address,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False,
    )

    # Download pre-processing parameters, unless they are already present
    parameter_path = os.path.join(TMP, model_parameter_object_key)
    if not os.path.isfile(parameter_path):
        minio_client.fget_object(
            bucket_name, model_parameter_object_key, parameter_path
        )
    with open(parameter_path, "rb") as pkl:
        params = pickle.load(pkl)

    all_categories = params["all_categories"]
    n_categories = params["n_categories"]
    all_letters = params["all_letters"]
    n_letters = params["n_letters"]

    # Download the model, unless already present
    model_path = os.path.join(TMP, model_object_key)
    if not os.path.isfile(model_path):
        minio_client.fget_object(bucket_name, model_object_key, model_path)

    # Load the model
    rnn_model = rnn.RNN(
        n_letters,
        128,
        n_letters,
        all_categories,
        n_categories,
        all_letters,
        n_letters,
    )
    rnn_model.load_state_dict(torch.load(model_path))
    rnn_model.eval()

    # Infer
    output_names = list(rnn_model.samples(language, start_letters))

    return {"output_names": output_names}
