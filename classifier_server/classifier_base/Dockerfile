# Set the base image to Python 3.10
FROM fedora:latest

RUN dnf install python3.10 pip -y

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies
#RUN pip install --no-cache-dir -r requirements.txt
