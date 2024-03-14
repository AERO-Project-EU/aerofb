# syntax=docker/dockerfile:1

ARG AERO_FB_TAG
FROM ckatsak/aerofb-alpine-base:${AERO_FB_TAG}
LABEL maintainer="ckatsak@cslab.ece.ntua.gr"

RUN pip install --no-cache-dir Flask gunicorn

CMD [ "python" ]
