import json
import random
import string
import time

import pyaes


def generate(length):
    letters = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters) for _ in range(length))


KEY = b"\xa1\xf6%\x8c\x87}_\xcd\x89dHE8\xbf\xc9,"


def function_handler(function_input):
    # Parse function input
    #payload = json.loads(function_input["payload"].decode("utf-8"))
    payload = json.loads(bytes(function_input["payload"]).decode("utf-8"))
    msg_len = int(payload["message_length"])
    num_iter = int(payload["num_iterations"])

    # Process input
    message = generate(msg_len)
    t_start = time.time_ns()
    for _ in range(num_iter):
        aes = pyaes.AESModeOfOperationCTR(KEY)
        ciphertext = aes.encrypt(message)

        aes = pyaes.AESModeOfOperationCTR(KEY)
        _ = aes.decrypt(ciphertext)

        aes = None
    t_end = time.time_ns()

    return {"encryption_iters_ns": t_end - t_start}
