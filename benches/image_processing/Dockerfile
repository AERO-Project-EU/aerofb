# syntax=docker/dockerfile:1

FROM ckatsak/aerofb-alpine-flask:0.0.1

COPY *.py /bench/
WORKDIR /bench/

RUN apk add --no-cache zlib-dev jpeg-dev libffi-dev \
    && pip install --no-cache-dir pillow minio
    #&& pip --no-cache-dir install -i https://test.pypi.org/simple/ ptpsync

CMD [ "gunicorn", "-b", "0.0.0.0", "-w", "1", "server:app" ]
