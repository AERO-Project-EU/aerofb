import json
import os.path
import time

import cv2

from minio import Minio


ACCESS_KEY = "minioroot"
SECRET_KEY = "minioroot"

TMP = "/tmp/"


def video_processing(video_path):
    result_file_path = video_path + ".avi"

    video = cv2.VideoCapture(video_path)

    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(result_file_path, fourcc, 20.0, (width, height))

    while video.isOpened():
        ret, frame = video.read()

        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            tmp_file_path = os.path.join(TMP, "tmp.jpg")
            cv2.imwrite(tmp_file_path, gray_frame)
            gray_frame = cv2.imread(tmp_file_path)
            out.write(gray_frame)
        else:
            break

    video.release()
    out.release()
    return result_file_path


def function_handler(function_input):
    # Parse function input
    #payload = json.loads(function_input["payload"].decode("utf-8"))
    payload = json.loads(bytes(function_input["payload"]).decode("utf-8"))
    minio_address = payload["minio_address"]
    bucket_name = payload["bucket_name"]
    vid_name = payload["vid_name"]
    vid_path = os.path.join(TMP, vid_name)

    # Download the input video from MinIO
    minio_client = Minio(
        minio_address,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False,
    )
    minio_client.fget_object(bucket_name, vid_name, vid_path)

    # Process input
    t_start = time.time_ns()
    # NOTE(ckatsak): vid2 needs more time than vid1
    out_file_path = video_processing(vid_path)
    t_end = time.time_ns()

    # Upload the output video to MinIO
    # NOTE(ckatsak): Let's just skip this so as not to stress networking/storage for
    # our experimentation
    # minio_client.fput_object(
    #     bucket_name, os.path.basename(out_file_path), out_file_path
    # )

    return {"processing_ns": t_end - t_start}
