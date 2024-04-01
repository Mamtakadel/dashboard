# Start from a python 3.10 image.
FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

#Creates a folder named code in / directory.
RUN mkdir -p /code

# Set the working directory
WORKDIR /code

# Copy just the dependency files from your project directory to /code inside docker image.
COPY requirement.txt /code/

#install dependencies
RUN pip install --no-cache-dir -r requirement.txt

# remove the requierement files once installed
RUN rm /code/requirement.txt

# Copy the rest of the application code
COPY . /code

# Expose port (if necessary)
EXPOSE 8000
# Command to run the application
CMD python3 manage.py runserver 0.0.0.0:8000
