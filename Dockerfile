FROM python:3.8-slim

# Install system dependencies including libGL
RUN apt-get update && apt-get install -y libgl1-mesa-glx

WORKDIR /app

# Copy all project files into the container
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

# Start the Flask app
CMD ["python", "app.py"]
