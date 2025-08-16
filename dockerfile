FROM python:3.11.10

# install ssh client
RUN apt-get update && apt-get install -y openssh-client

# set enviroment variables
ENV PYTHONUNBUFFERED=1

# set the working directory
WORKDIR /app

# copy the requirements file
COPY requirements.txt /app/requirements.txt

# install python dependencies
RUN pip install -r requirements.txt


# copy the applicacion to the working directory
COPY . /app

# start the SSH tunnel
CMD  python manage.pu runserver 0.0.0.0:8000