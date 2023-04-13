FROM python:3

WORKDIR /Docker

COPY requirements.txt /Docker
RUN pip install --no-cache-dir -r requirements.txt

COPY . /Docker
RUN mkdir ./docker_src/database

CMD [ "python", "./docker_src/main.py" ]
