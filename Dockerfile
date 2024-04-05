# # Start from a python 3.10 image.
# FROM python:3.10-slim

# ENV PYTHONUNBUFFERED 1

# #Creates a folder named code in / directory.
# RUN mkdir -p /code

# # Set the working directory
# WORKDIR /code

# # Copy just the dependency files from your project directory to /code inside docker image.
# COPY requirement.txt /code/

# #install dependencies
# RUN pip install --no-cache-dir -r requirement.txt
# RUN apt-get update && apt-get install -y gdal-bin libgdal-dev

# # remove the requierement files once installed
# RUN rm /code/requirement.txt

# # Copy the rest of the application code
# COPY . /code

# # Expose port (if necessary)
# EXPOSE 8000
# # Command to run the application
# CMD python3 manage.py runserver 0.0.0.0:8000


# FROM python:3
# # Starts from python:3 Image
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# # Sets some env vars.
# # I need a directory inside image to put my code, so i make a directory called code.
# RUN mkdir /code
# # Now this code directory is created, i need this dir to be my working dir.
# WORKDIR /code
# # Now i have my /code as a default dir, I am going to copy all my code inside this dir.
# COPY . /code/
# RUN apt-get update && apt-get install -y gdal-bin libgdal-dev
# # Now i have my code, i will install packages from requirements.txt
# RUN pip3 install -r requirements.txt
# # Now i have my dependencies  installed, i will try to run my django app.
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM naxa/python:3.9-slim
# Uses naxa/python:3.9-slim instead of python:3.9-slim so that
# apt/requirement doesn't have to reinstall everytime

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code
RUN mkdir -p /sock
RUN mkdir -p /logs
WORKDIR /code

COPY apt_requirements.txt /code/
RUN apt-get -y update
RUN cat apt_requirements.txt | xargs apt -y --no-install-recommends install && \
	rm -rf /var/lib/apt/lists/* && \
	apt autoremove && \
	apt autoclean

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

COPY requirements.txt /code/

#required for gdal installation
RUN pip install --no-cache-dir setuptools==57.5.0
RUN pip install --no-cache-dir -r requirements.txt
RUN rm /code/requirements.txt /code/apt_requirements.txt

COPY . /code

COPY entrypoint.sh /code/entrypoint.sh
