# Base image with Python and CUDA for GPU support
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install specific versions of critical libraries
RUN pip install torch==2.0.1+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
RUN pip install transformers==4.33.3
RUN pip install peft==0.5.0

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app_feed.py", "--server.port=8501", "--server.address=0.0.0.0"]