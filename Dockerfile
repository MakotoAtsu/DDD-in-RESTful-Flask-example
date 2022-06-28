FROM python:3.10.5-buster

COPY ./requirements.txt /todo_service/requirements.txt

RUN pip install --no-cache-dir -r /todo_service/requirements.txt && \
    pip install gunicorn && \
    apt-get update && \
    apt-get install net-tools

COPY . /todo_service

WORKDIR /todo_service
EXPOSE 8000

CMD [ "gunicorn" ,"--bind=0.0.0.0:8000" ,"--timeout=600" , "wsgi:app" ]
