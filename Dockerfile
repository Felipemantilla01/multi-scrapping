# Base Image
FROM python:3.8.5

# create and set working directory
RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory
ADD . /app/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 

# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here
ENV PORT=8000

# Install system dependencies
RUN apt-get update && apt-get -y install cron
RUN apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# install environment dependencies
RUN pip3 install --upgrade pip 
RUN pip3 install pipenv

# Install project dependencies
RUN pipenv install --skip-lock --system --dev --ignore-pipfile --deploy

# Copy hello-cron file to the cron.d directory
COPY hello-cron /etc/cron.d/hello-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron
RUN chmod 0644 /app/cron.sh

# Apply cron job
RUN crontab /etc/cron.d/hello-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
# CMD cron && tail -f /var/log/cron.log
# CMD cron
RUN service cron start

EXPOSE 8000
# CMD gunicorn cfehome.wsgi:application --bind 0.0.0.0:$PORT
CMD python manage.py runserver 0.0.0.0:$PORT