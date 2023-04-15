FROM classifier_server_classifier_base

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install waitress

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Start the Flask server
CMD ["waitress-serve", "--host=0.0.0.0", "--port=8000", "app:app"]
