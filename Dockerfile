# Build stage
FROM --platform=$BUILDPLATFORM public.ecr.aws/docker/library/python:3.9-slim AS builder

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    && pip wheel --no-cache-dir --wheel-dir=/app/wheels -r requirements.txt

# Runtime stage
FROM --platform=$TARGETPLATFORM public.ecr.aws/docker/library/python:3.9-slim

WORKDIR /app

# Copy only necessary files
COPY --from=builder /app/wheels /app/wheels
COPY . .

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    curl \
    && pip install --no-cache-dir --no-index --find-links=/app/wheels -r requirements.txt \
    && rm -rf /app/wheels \
    && rm -rf /var/lib/apt/lists/*

# Add local bin to PATH
# ENV PATH=/root/.local/bin:$PATH

# Create non-root user
RUN useradd -m streamlit
RUN chown -R streamlit:streamlit /app
USER streamlit

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Start application
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]