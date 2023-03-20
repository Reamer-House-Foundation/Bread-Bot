ARG BASE_IMAGE

# Set the base image to Python 3.10
#FROM ${BASE_IMAGE}
FROM classifier_server_classifier_base

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Start the Flask server
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
