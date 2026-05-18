FROM python:3.12-slim

WORKDIR /app

# 1. Install required system dependencies (like gcc and postgres headers)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of the application
COPY . .

EXPOSE 5000

# Remember: Do not use 'flask run' in production! 
# This is okay for local docker-compose development.
CMD ["flask", "run", "--host=0.0.0.0"]