
FROM python:3.9

# Set working directory
WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    gcc \
    build-essential \
    mariadb-client-compat \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements folder (both base.txt and dev.txt)
COPY requirements/ ./requirements/

# Install dev/test dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements/dev.txt

# Copy project files
COPY . .

# Expose Django port
EXPOSE 8000

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

