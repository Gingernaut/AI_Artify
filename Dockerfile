FROM alpine:3.6

## pip3 install -r py3reqs.txt
## pip install -r py2reqs.txt

RUN apk add --update \
    python \
    python3 \
    python-dev \
    py-pip \
    build-base \
  && rm -rf /var/cache/apk/*

WORKDIR /app

COPY . /app
RUN pip install -r /app/py2reqs.txt && pip3 install /app/py3reqs.txt
RUN pip install https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.11.0rc1-cp35-cp35m-linux_x86_64.whl

EXPOSE 5000
CMD ["/usr/bin/python", "main.py"]