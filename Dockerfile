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

# Copy application code
COPY . .

# Copy and setup Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /var/log/nginx && \
    mkdir -p /run && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /run && \
    chmod 755 /var/log/nginx

# Create startup script
RUN echo '#!/bin/bash\n\
# Replace environment variables in nginx.conf\n\
envsubst "\$NGINX_MAX_BODY_SIZE \$NGINX_PROXY_READ_TIMEOUT" < /etc/nginx/nginx.conf > /etc/nginx/nginx.conf.tmp \n\
mv /etc/nginx/nginx.conf.tmp /etc/nginx/nginx.conf\n\
\n\
# Start Nginx\n\
nginx &\n\
\n\
# Start Streamlit\n\
streamlit run main.py --server.port=8501 --server.address=127.0.0.1\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8501

# Start Nginx and Streamlit
CMD ["/app/start.sh"]