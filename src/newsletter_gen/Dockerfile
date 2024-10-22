FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory
COPY . /app/

# Set environment variable for the port
ENV PORT=8080

# Expose the port
EXPOSE 8080

# Ensure Python can find the newsletter_gen module
ENV PYTHONPATH=/app/

# Use the PORT environment variable in the command
CMD exec python main.py