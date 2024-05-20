# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip3 install --requirement ./requirements.txt
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run server.py when the container launches
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]