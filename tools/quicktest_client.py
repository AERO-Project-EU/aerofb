#!/usr/bin/env python3

import json
import os
import sys
import time

import click
import requests


DEFAULT_ADDRESS = "localhost:8000"


@click.command()
@click.option(
    "-k",
    "--knative",
    "host_port",
    metavar="HOST:PORT",
    default=lambda: os.environ.get("HOSTPORT", DEFAULT_ADDRESS),
    show_default=DEFAULT_ADDRESS,
    type=str,
    prompt="HOST:PORT",
    help="Server address & port",
)
@click.argument("bench")
def invoke(host_port: str, bench: str) -> int:
    addr, port = host_port.split(":")
    url = (
        "http://"
        + (
            f'aerofb-{bench.replace("_", "-")}-fc.default.{addr}.sslip.io'
            if addr != "localhost"
            else "localhost"
        )
        + f":{port}/invoke"
    )
    click.secho(f"URL: {url}", fg="blue")

    click.secho(f"INPUT: {json.dumps(TEST_INPUT[bench])}", fg="yellow")

    start_ts = time.perf_counter_ns()
    resp = requests.post(url, json=TEST_INPUT[bench])
    end_ts = time.perf_counter_ns()

    if 200 <= resp.status_code < 300:
        click.secho(f"\n{resp}", fg="green", bold=True)
        click.secho(resp.json(), fg="green")
        click.secho(
            f"Client-perceived latency: {end_ts - start_ts} ns", fg="cyan"
        )
        return 0
    else:
        click.secho(f"\n{resp}", bg="red", bold=True)
        click.secho(resp.content.decode(), fg="red")
        return 1


MINIO_ADDRESS = os.getenv("MINIO_ADDRESS") or "icy1.cslab.ece.ntua.gr:59000"
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME") or "snaplace-fbpml"

NROW, NCOL = 10, 15
OPS = ["filter", "flip", "gray_scale", "resize", "rotate"]
JSON_FILE = "search.json"
MODEL_OBJECT_KEY = "lr_model_reviews10mb.pk"
TFIDF_VECT_OBJECT_KEY = "lr_vectorizer_reviews10mb.pk"
X = "The ambiance is magical. The food and service was nice! The lobster and cheese was to die for and our steaks were cooked perfectly.  "  # noqa
DATASET_OBJECT_KEY = "reviews10mb.csv"
N = M = 512
MESSAGE_LENGTH, NUM_ITERATIONS = 1024, 32
LANGUAGE, START_LETTERS, MODEL_PARAMETER_OBJ_KEY, MODEL_OBJ_KEY = (
    "Greek",
    "QRSTUVWXYZABCDEF",
    "rnn_params.pkl",
    "rnn_model.pth",
)
VID_NAME = "big_buck_bunny_360p_1mb.mp4"
IMG_IDX = 0


def payloadize(d):
    return list(json.dumps(d).encode())


TEST_INPUT = {
    "helloworld": {},
    "chameleon": {
        "payload": payloadize({"nrow": NROW, "ncol": NCOL}),
        "metadata_map": {"header-nrow": str(NROW), "header-ncol": str(NCOL)},
    },
    "cnn_serving": {
        "payload": payloadize({"img_idx": IMG_IDX}),
        "metadata_map": {"header-img-idx": str(IMG_IDX)},
    },
    "image_processing": {
        "payload": payloadize(
            {
                "minio_address": MINIO_ADDRESS,
                "bucket_name": MINIO_BUCKET_NAME,
                "img_name": "img230k.jpeg",
                "ops": "-".join(OPS),
            }
        ),
        "metadata_map": {
            "header-minio-address": MINIO_ADDRESS,
            "header-bucket-name": MINIO_BUCKET_NAME,
            "header-img-name": "img230k.jpeg",
            "header-ops": "-".join(OPS),
        },
    },
    "json_serdes": {
        "payload": payloadize(
            {
                "minio_address": MINIO_ADDRESS,
                "bucket_name": MINIO_BUCKET_NAME,
                "file_name": JSON_FILE,
            }
        ),
        "metadata_map": {
            "header-minio-address": MINIO_ADDRESS,
            "header-bucket-name": MINIO_BUCKET_NAME,
            "header-file-name": JSON_FILE,
        },
    },
    "lr_serving": {
        "payload": payloadize(
            {
                "minio_address": MINIO_ADDRESS,
                "bucket_name": MINIO_BUCKET_NAME,
                "model_object_key": MODEL_OBJECT_KEY,
                "tfidf_vect_object_key": TFIDF_VECT_OBJECT_KEY,
                "x": X,
            }
        ),
        "metadata_map": {
            "header-minio-address": MINIO_ADDRESS,
            "header-bucket-name": MINIO_BUCKET_NAME,
            "header-model-object-key": MODEL_OBJECT_KEY,
            "header-tfidf-vect-object-key": TFIDF_VECT_OBJECT_KEY,
            "header-x": X,
        },
    },
    "lr_training": {
        "payload": payloadize(
            {
                "minio_address": MINIO_ADDRESS,
                "bucket_name": MINIO_BUCKET_NAME,
                "dataset_object_key": DATASET_OBJECT_KEY,
            }
        ),
        "metadata_map": {
            "header-minio-address": MINIO_ADDRESS,
            "header-bucket-name": MINIO_BUCKET_NAME,
            "header-dataset-object-key": DATASET_OBJECT_KEY,
        },
    },
    "matmul": {
        "payload": payloadize({"N": N, "M": M}),
        "metadata_map": {"header-N": str(N), "header-M": str(M)},
    },
    "pyaes": {
        "payload": payloadize(
            {
                "message_length": MESSAGE_LENGTH,
                "num_iterations": NUM_ITERATIONS,
            }
        ),
        "metadata_map": {
            "header-message-length": str(MESSAGE_LENGTH),
            "header-num-iterations": str(NUM_ITERATIONS),
        },
    },
    "rnn_serving": {
        "payload": payloadize(
            {
                "minio_address": MINIO_ADDRESS,
                "bucket_name": MINIO_BUCKET_NAME,
                "language": LANGUAGE,
                "start_letters": START_LETTERS,
                "model_parameter_object_key": MODEL_PARAMETER_OBJ_KEY,
                "model_object_key": MODEL_OBJ_KEY,
            }
        ),
        "metadata_map": {
            "header-minio-address": MINIO_ADDRESS,
            "header-bucket-name": MINIO_BUCKET_NAME,
            "header-language": LANGUAGE,
            "header-start-letters": START_LETTERS,
            "header-model-param-obj-key": MODEL_PARAMETER_OBJ_KEY,
            "header-model-object-key": MODEL_OBJ_KEY,
        },
    },
    "video_processing": {
        "payload": payloadize(
            {
                "minio_address": MINIO_ADDRESS,
                "bucket_name": MINIO_BUCKET_NAME,
                "vid_name": VID_NAME,
            }
        ),
        "metadata_map": {
            "header-minio-address": MINIO_ADDRESS,
            "header-bucket-name": MINIO_BUCKET_NAME,
            "header-vid-name": VID_NAME,
        },
    },
}


if __name__ == "__main__":
    sys.exit(invoke())
