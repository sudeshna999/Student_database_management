# Use the official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install virtualenv
RUN pip install virtualenv

# Create a virtual environment
RUN virtualenv venv

# Activate the virtual environment and install dependencies
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy the application source code to the container
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]