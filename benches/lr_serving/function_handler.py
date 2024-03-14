import json
import os.path
import re

import joblib
import pandas as pd
from minio import Minio


ACCESS_KEY = "minioroot"
SECRET_KEY = "minioroot"

TMP = "/tmp/"

cleanup_re = re.compile("[^a-z]+")


def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(" ", sentence).strip()
    return sentence


def function_handler(function_input):
    # Parse function input
    #payload = json.loads(function_input["payload"].decode("utf-8"))
    payload = json.loads(bytes(function_input["payload"]).decode("utf-8"))
    minio_address = payload["minio_address"]
    bucket_name = payload["bucket_name"]
    model_object_key = payload[
        "model_object_key"
    ]  # e.g., lr_model_reviews10mb.pk
    tfidf_vect_object_key = payload[
        "tfidf_vect_object_key"
    ]  # e.g., lr_vectorizer_reviews10mb
    x = payload["x"]

    minio_client = Minio(
        minio_address,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False,
    )

    # In case of cold starts, the model and the tfidf vectorizer will have
    # to be initialized (i.e., downloaded from the store according to
    # function_input). Subsequent calls will not need to go through this.
    model_file_path = os.path.join(TMP, model_object_key)
    if not os.path.isfile(model_file_path):
        minio_client.fget_object(
            bucket_name, model_object_key, model_file_path
        )
    model = joblib.load(model_file_path)

    tfidf_vect_file_path = os.path.join(TMP, tfidf_vect_object_key)
    if not os.path.isfile(tfidf_vect_file_path):
        minio_client.fget_object(
            bucket_name, tfidf_vect_object_key, tfidf_vect_file_path
        )
    tfidf_vect = joblib.load(tfidf_vect_file_path)

    # Process input
    df_input = pd.DataFrame()
    df_input["x"] = [x]
    df_input["x"] = df_input["x"].apply(cleanup)
    X = tfidf_vect.transform(df_input["x"])

    y = model.predict(X)

    return {"y": y.tolist()}
