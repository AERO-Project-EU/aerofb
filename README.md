# AERO FunctionBench

[![ghcri.io.yml-main](https://github.com/ckatsak/aerofb/actions/workflows/ghcr.io.yml/badge.svg?branch=main)](.github/workflows/ghcr.io.yml)

AERO port of Serverless functions adopted from the [original
FunctionBench](https://github.com/ddps-lab/serverless-faas-workbench) FaaS
benchmarking suite for multi-arch image builds.

Functions speak JSON and are served over plain HTTP (`Flask` + `gunicorn`).

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

## License

Licensed under the terms of Apache License, Version 2.0.

For more information, consult the included [LICENSE](LICENSE) file.

## Acknowledgments

This work is supported by the European Commission under the Horizon Europe grant 101092850 (project AERO).
