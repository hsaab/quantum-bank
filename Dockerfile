# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application code
COPY . .

# Run the app as a non-root user.
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
RUN chown -R appuser:appgroup /app
USER appuser

# Make port 10000 available (Render's default)
EXPOSE 10000

# Run with gunicorn for production
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app