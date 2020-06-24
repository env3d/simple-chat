from python:3.7

RUN pip install boto3
RUN pip install paramiko
RUN pip install passlib
RUN pip install python-dotenv
RUN pip install flask
RUN pip install gunicorn
RUN pip install Flask-Sockets

COPY ./src /opt/simple-chat/src

WORKDIR /opt/simple-chat/src
