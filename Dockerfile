# Build stage
FROM --platform=$BUILDPLATFORM public.ecr.aws/docker/library/python:3.9-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir=/app/wheels -r requirements.txt

# Runtime stage
FROM --platform=$TARGETPLATFORM public.ecr.aws/docker/library/python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    curl \
    gettext-base \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -r nginx  # Create nginx user

# Set working directory
WORKDIR /app

# Copy wheels from builder
COPY --from=builder /app/wheels /app/wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/app/wheels -r requirements.txt \
    && rm -rf /app/wheels

# Copy Gunicorn config
COPY gunicorn_config.py .

# Copy application code
COPY . .

# Copy and setup Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /var/log/nginx && \
    mkdir -p /var/log/gunicorn && \
    mkdir -p /run && \
    mkdir -p logs && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /run && \
    chown -R www-data:www-data /var/log/gunicorn && \
    chown -R www-data:www-data logs && \
    chmod 755 /var/log/nginx && \
    chmod 755 /var/log/gunicorn && \
    chmod 755 logs

# Create startup script with environment variable substitution
RUN echo '#!/bin/bash\n\
# Set default values for environment variables\n\
export NGINX_MAX_BODY_SIZE=${NGINX_MAX_BODY_SIZE:-10M}\n\
export NGINX_PROXY_READ_TIMEOUT=${NGINX_PROXY_READ_TIMEOUT:-86400}\n\
\n\
# Replace environment variables in nginx.conf\n\
envsubst "\$NGINX_MAX_BODY_SIZE \$NGINX_PROXY_READ_TIMEOUT" < /etc/nginx/nginx.conf > /etc/nginx/nginx.conf.tmp \n\
mv /etc/nginx/nginx.conf.tmp /etc/nginx/nginx.conf\n\
\n\
# Start Nginx\n\
nginx &\n\
\n\
# Start Gunicorn\n\
gunicorn -c gunicorn_config.py app:app\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port 80
EXPOSE 80

# Start Nginx and Gunicorn
CMD ["/app/start.sh"]