# CYBER-DEF25 Challenge - Malware Detection Container
# Dockerfile for AI-based Malware Detection System

# Use official Python runtime as base image
FROM python:3.9-slim

# Set metadata labels
LABEL maintainer="CYBER-DEF25 Participant"
LABEL description="AI-based Malware Detection Inference Container"
LABEL version="1.0"

# Set working directory in container
WORKDIR /app

# Create necessary directories for input and output
RUN mkdir -p /input/logs /output

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the trained model
COPY model.pkl .

# Copy the inference script
COPY inference.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/model.pkl
ENV INPUT_DIR=/input/logs
ENV OUTPUT_DIR=/output

# Make inference script executable
RUN chmod +x inference.py

# Set the default command to run the inference script
CMD ["python", "inference.py"]
