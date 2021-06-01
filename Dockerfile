FROM python:3.9.5
WORKDIR /src
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .