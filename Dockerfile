FROM phusion/baseimage:latest

CMD ["/sbin/my_init"]

WORKDIR /app

COPY py*.txt /

RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && \
    apt-get install -y python3.6 python-pip python3-pip python3-dev

RUN pip install --upgrade pip==9.0.3 && \
    pip install -r /py2reqs.txt && \
    pip3 install -r /py3reqs.txt

RUN mkdir -p /app/images/input && mkdir -p /app/images/output
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . /app


CMD ["python3","/app/main.py"]
