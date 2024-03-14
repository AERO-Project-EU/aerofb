# syntax=docker/dockerfile:1

FROM docker.io/library/python:3.12-alpine3.19
LABEL maintainer="ckatsak@cslab.ece.ntua.gr"

RUN apk add --no-cache --update g++ musl-dev make linux-headers openblas-dev lapack-dev \
    && pip install --no-cache-dir pandas scikit-learn

CMD [ "python" ]
