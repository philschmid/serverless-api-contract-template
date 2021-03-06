FROM python:3.8.2-slim

# set working directory 
WORKDIR /app

# copy only the requirements.txt

COPY ./requirements.txt /app/requirements.txt


# Install production dependencies.
RUN apt-get update -y \
    && apt-get install -y gcc libpq-dev \
    && pip install --no-cache-dir gunicorn \
    && pip install -r requirements.txt --no-cache-dir

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True



# Copy local code to the container image.
COPY . /app




# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD gunicorn main:app -c gunicorn_config.py