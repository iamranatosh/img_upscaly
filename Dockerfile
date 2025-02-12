FROM python:3.8-slim

# Update package lists and install system dependencies including libGL and libglib2.0-0
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

WORKDIR /app

# Copy all project files into the container
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

# Start the Flask app
CMD ["python", "app.py"]
