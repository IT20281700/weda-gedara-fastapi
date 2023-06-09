FROM python:3.11.3-slim

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD uvicorn main:app --port=9001 --host=0.0.0.0