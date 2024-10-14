FROM python:3.12.0-slim

RUN apt-get update && apt-get install -y mc

RUN mkdir /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt --no-cache-dir

COPY proj/ /app
WORKDIR /app

CMD ["python", "manage.py", "runserver", "0:8000"]
