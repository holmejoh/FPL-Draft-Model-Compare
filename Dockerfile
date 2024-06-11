# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define an argument for names during build
ARG NAMES

# Pass names as an environment variable to the container
ENV NAMES="${NAMES}"

# Run main.py when the container launches
CMD ["python", "main.py"]