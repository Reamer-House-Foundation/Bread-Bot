# Use the official Node.js image as the base image
FROM node:16

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json into the working directory
COPY package*.json ./

# Install the dependencies
RUN npm ci

# Copy the rest of the application code into the working directory
COPY . .

# Expose the port your app will run on
EXPOSE 3000

# Start the application
CMD ["node", "index.js"]
