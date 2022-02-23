#Dockerfile for cleanMyData-POC

FROM debian:11.1

RUN apt update \
&& apt install -y python3 python3-pip python3-dev build-essential

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt

COPY p6/ /usr/src/app/

CMD ["python3", "/usr/src/app/start.py"]
