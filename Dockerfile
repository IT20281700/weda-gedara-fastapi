FROM python:3.11.3-slim

WORKDIR /app
COPY . /app
# RUN pip install --upgrade pip
# RUN python -m pip install wheel setuptools pip --upgrade
RUN pip install -r requirements.txt

CMD uvicorn main:app --port=9001 --host=0.0.0.0