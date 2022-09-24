# The base image to use - here we're using a pre-built python one
# FROM - initializes a new build stage and sets the Base Image for subsequent instructions
FROM python:3.10

# Set a directory for the app
# WORKDIR -  define the working directory of a Docker container at any given time
WORKDIR /usr/src/app

# Copy all the files to the container
# COPY - copies files from a local source location to a destination in the Docker container
COPY . .

# run the script 
# (we have to use -u here to let the program run in the background)
# CMD - specifies the default program that will execute once the container runs
CMD ["python", "-u", "./main.py"]