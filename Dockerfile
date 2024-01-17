FROM python:3.12-slim-buster


WORKDIR .
RUN apt -qq update && apt -qq install -y git wget pv jq python3-dev ffmpeg mediainfo aria2 curl node.js npm
COPY . .
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt
RUN apt install ffmpeg aria2

CMD ["python3", "main.py"]
