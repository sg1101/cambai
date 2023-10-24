# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies from the requirements file
RUN pip install -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose the port that your FastAPI application will run on
EXPOSE 8000

## Command to run your FastAPI application
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
