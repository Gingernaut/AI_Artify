FROM phusion/baseimage:0.9.19

CMD ["/sbin/my_init"]

COPY . /app
WORKDIR /app

ENV PROJECT=ai_artify

RUN apt-get update && apt-get install -y python3 python-pip python3-pip python3-dev
RUN pip install -r /app/py2reqs.txt
RUN pip3 install -r /app/py3reqs.txt
RUN mkdir -p /app/images/input
RUN mkdir -p /app/images/output

EXPOSE 5000
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
CMD ["python3","/app/main.py"]
