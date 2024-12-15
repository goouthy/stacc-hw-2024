FROM python:3.10-slim

# Working dir inside container
WORKDIR /iris

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copying app, tests, data dirs into /iris
COPY app /iris/app
COPY tests /iris/tests
COPY data /iris/data

EXPOSE 5000

CMD ["python", "app/main.py"]