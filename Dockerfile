FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask flask-sock pymongo

# Expose port for Flask
EXPOSE 3000

# Expose port for Socket server
EXPOSE 5000

# Run the main application
CMD ["python", "main.py"]
