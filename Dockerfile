# Use official Python image as a base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies for Tesseract and Pillow
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /iid
WORKDIR /iitd

# Copy the requirements file into the container
COPY requirements.txt /iitd/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . /iid

# Expose port 8000
EXPOSE 8000

# Run the Flask app
CMD ["python", "app.py"]
