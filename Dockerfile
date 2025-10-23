# ==============================
# Stage 1: Build environment
# ==============================
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8000

# Run database migrations and collect static files
RUN python manage.py migrate --noinput || true
RUN python manage.py collectstatic --noinput || true

# Start server using Gunicorn
CMD ["gunicorn", "eventmanagementwebapp.wsgi:application", "--bind", "0.0.0.0:8000"]
