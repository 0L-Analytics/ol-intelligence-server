FROM python:3.9-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/src/app

# set workdir
WORKDIR /usr/src/app

# create .0L dir
RUN mkdir -p /root/.0L
COPY assets/0L.toml /root/.0L/

# copy binaries
COPY ./bin /usr/src/app/bin

# make executable
RUN chmod +x /usr/src/app/bin/ol

# add ol path to PATH
ENV PATH "$PATH:/usr/src/app/bin"

# install dependencies
RUN apt-get update \
&& apt-get install -y \
  python3-dev \
  python3-pip \
  gcc \
  libc-dev \
  libffi-dev \
  netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy app
COPY ./src /usr/src/app/src
COPY ./manage.py /usr/src/app

# ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# run application
# CMD ["tail", "-f", "/dev/null"]
# CMD ["python3", "manage.py", "run", "-h", "0.0.0.0"]

