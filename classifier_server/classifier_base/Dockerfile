# Use pytorch as a base image.  This is based off of debian and includes
# python3.10 as well as pip
FROM pytorch/pytorch

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt
