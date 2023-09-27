# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required packages
RUN pip install --no-cache-dir flask requests

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables for ServiceNow credentials
# These will be passed when starting the container
ENV SERVICE_NOW_USERNAME=your_username
ENV SERVICE_NOW_PASSWORD=your_password

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
