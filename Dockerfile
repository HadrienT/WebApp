# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /docker_root

# Copy the requirements files into the container
COPY requirements.txt setup.py pyproject.toml setup.cfg ./

# Copy the rest of the application code into the container
COPY src ./src

# Install any needed packages specified in requirements.txt and requirements_dev.txt
RUN pip install -r requirements.txt --no-cache
RUN pip install -e . --no-cache


# Expose the port the app runs on
EXPOSE 8000

# Run the command to start the app using Uvicorn
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
