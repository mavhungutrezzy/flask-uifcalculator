# Use official Python image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0


# Run the application using Gunicorn
CMD ["gunicorn", "--workers", "4", "--threads", "2", "--timeout", "120", "-b", "0.0.0.0:5000", "app:app"]
