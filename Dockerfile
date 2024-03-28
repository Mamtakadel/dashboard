# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirement.txt /app/
RUN pip install -r requirement.txt

# Copy the project code into the container
COPY . /app/
CMD python3 manage.py runserver