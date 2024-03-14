import json

# import tensorflow as tf
# from keras.preprocessing import image
from keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.applications.resnet50 import (
    preprocess_input,
    decode_predictions,
)
import numpy as np

from squeezenet import SqueezeNet

model = SqueezeNet(weights="imagenet")
model.make_predict_function()
print("Model is ready")

# img1 = load_img("/bench/cnn_img1.jpeg", target_size=(227, 227))
# img2 = load_img("/bench/cnn_img2.jpeg", target_size=(227, 227))
# imgs = [img1, img2]

IMG_PATHS = ["/bench/cnn_img1.jpeg", "/bench/cnn_img2.jpeg"]

######### maybe
# x = img_to_array(img1)
# x = np.expand_dims(x, axis=0)
# x = preprocess_input(x)
# preds = model1.predict(x)
######### maybe


def function_handler(function_input):
    # idx = request.arg if request.arg and 0 <= request.arg <= 1 else 0
    #
    # img = imgs[idx]
    # model = models[idx]
    #
    # x = img_to_array(img)
    # x = np.expand_dims(x, axis=0)
    # x = preprocess_input(x)
    # preds = model.predict(x)
    #
    ## _ = decode_predictions(preds)  # requires network & local storage
    #
    # return {"preds": preds.tolist()}

    # Parse function input
    #payload = json.loads(function_input["payload"].decode("utf-8"))
    payload = json.loads(bytes(function_input["payload"]).decode("utf-8"))
    # minio_address = payload["minio_address"]
    # bucket_name = payload["bucket_name"]
    # img_name = payload["img_name"]
    # img_path = os.path.join(TMP, img_name)
    idx = int(payload["img_idx"])

    # img = imgs[idx]
    img = load_img(IMG_PATHS[idx], target_size=(227, 227))

    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)

    # result = decode_predictions(preds)  # requires network & local storage

    return {"preds_len": len(preds.tolist())}
