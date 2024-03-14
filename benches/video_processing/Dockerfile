# syntax=docker/dockerfile:1

FROM ckatsak/opencv-slim:4.9.0-python3.12.2-slim-bookworm

COPY *.py /bench/
WORKDIR /bench

RUN pip install --no-cache-dir opencv-python minio Flask gunicorn
    #&& pip --no-cache-dir install -i https://test.pypi.org/simple/ ptpsync

CMD [ "gunicorn", "-b", "0.0.0.0", "-w", "1", "server:app" ]
