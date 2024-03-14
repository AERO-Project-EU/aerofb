import json
import os
import os.path
import re
import time

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd

from minio import Minio


ACCESS_KEY = "minioroot"
SECRET_KEY = "minioroot"

TMP = "/tmp"

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
    dataset_object_key = payload["dataset_object_key"]

    latencies_ns = {}

    # Download input dataset, unless already present
    t_start = time.perf_counter_ns()
    dataset_file_path = os.path.join(TMP, dataset_object_key)
    if not os.path.isfile(dataset_file_path):
        minio_client = Minio(
            minio_address,
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            secure=False,
        )
        minio_client.fget_object(
            bucket_name, dataset_object_key, dataset_file_path
        )
    latencies_ns["download"] = time.perf_counter_ns() - t_start

    # Process input
    df = pd.read_csv(dataset_file_path)
    t_start = time.perf_counter_ns()
    df["train"] = df["Text"].apply(cleanup)
    tfidf_vector = TfidfVectorizer(min_df=100).fit(df["train"])
    train = tfidf_vector.transform(df["train"])
    model = LogisticRegression()
    model.fit(train, df["Score"])
    latencies_ns["training"] = time.perf_counter_ns() - t_start

    # Serialize the model and the vectorizer to local files
    suffix = time.time_ns()  # ¿FIXME: from function_input instead?
    # Rather than uploading the file, further stressing the network (mostly),
    # we just unlink the local files after being dumped through joblib. XXX
    model_object_key = f"lr_model_{suffix}.pk"
    model_file_path = os.path.join(TMP, model_object_key)
    joblib.dump(model, model_file_path)
    # minio_client.fput_object(bucket_name, model_object_key, model_file_path)
    # Same for the TfidfVectorizer
    vectorizer_object_key = f"lr_vectorizer_{suffix}.pk"
    vectorizer_file_path = os.path.join(TMP, vectorizer_object_key)
    joblib.dump(tfidf_vector, vectorizer_file_path)
    # minio_client.fput_object(
    #    bucket_name, vectorizer_object_key, vectorizer_file_path
    # )
    os.remove(model_file_path)
    os.remove(vectorizer_file_path)

    return {"latencies_ns": latencies_ns}
