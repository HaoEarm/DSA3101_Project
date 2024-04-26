# Use an official Python runtime as a base image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8050 available to the world outside this container
EXPOSE 8050

# Define environment variable for Flask to run in production mode
ENV FLASK_ENV=production

# Run app.py using Flask's built-in server
CMD ["python", "app.py"]