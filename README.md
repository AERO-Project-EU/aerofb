# AERO FunctionBench

> [!NOTE]
> Similar to `ckatsak/snaplace-fbpml`, but using plain JSON over HTTP (`Flask` +
> `gunicorn`) instead of `protobuf` over `gRPC` (over HTTP/2).

## Porting Status

|     benchmark    |   `amd64` build  |   `amd64` test   | `aarch64` build  |  `aarch64` test  |
|:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|
|   `helloworld`   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|    `chameleon`   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|   `cnn_serving`  |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|`image_processing`|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|   `json_serdes`  |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|   `lr_serving`   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|   `lr_training`  |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|      `matmul`    |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|      `pyaes`     |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|   `rnn_serving`  |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|`video_processing`|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
