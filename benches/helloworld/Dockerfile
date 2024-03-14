# syntax=docker/dockerfile:1

FROM ckatsak/aerofb-alpine-flask:0.0.1

COPY *.py /bench/
WORKDIR /bench

CMD [ "gunicorn", "-b", "0.0.0.0", "-w", "1", "server:app" ]
