# Stage 1: Build dependencies
FROM python:3.10-slim AS builder

WORKDIR /app

# Install required dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Create final lightweight image
FROM python:3.10-slim

WORKDIR /app

# Set environment variables for Streamlit and Python optimizations
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS="0.0.0.0" \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Copy only necessary files from the builder stage
COPY --from=builder /install /usr/local
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
