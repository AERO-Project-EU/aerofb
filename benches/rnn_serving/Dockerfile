# syntax=docker/dockerfile:1

FROM bitnami/pytorch:1.13.1-debian-11-r29
# amd64: sha256:498c55bd19ffe283452fa66ae80774ce5f0d6ba4c20c5dd6205d32f5d0647fd8
# arm64/v8: sha256:38702e32a108cc22bf842bcbcbd8375cddf98e08bf7168f997ab3d7270dbff34

USER root:root
COPY *.py /bench/
WORKDIR /bench

RUN pip install --no-cache-dir minio Flask gunicorn \
    && ln -sf /opt/bitnami/python/bin/python3 /usr/local/bin/python \
    && ln -sf /opt/bitnami/python/bin/python3 /usr/local/bin/python3
    #&& pip --no-cache-dir install -i https://test.pypi.org/simple/ ptpsync \

CMD [ "gunicorn", "-b", "0.0.0.0", "-w", "1", "server:app" ]
