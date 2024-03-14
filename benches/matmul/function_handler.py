import json
import time

import numpy as np


def function_handler(function_input):
    # Parse function input
    #payload = json.loads(function_input["payload"].decode("utf-8"))
    payload = json.loads(bytes(function_input["payload"]).decode("utf-8"))
    N = int(payload["N"])
    M = int(payload["M"])

    # Process input
    A = np.random.rand(N, M)  # NxM
    B = np.random.rand(M, M)  # MxN

    t_start = time.time_ns()
    _ = np.matmul(A, B)  # NxN
    t_end = time.time_ns()

    return {"processing_ns": t_end - t_start}
