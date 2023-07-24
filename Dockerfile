FROM python:3.10

EXPOSE 80

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./datahub /src/app

COPY .run.py /src/run.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
