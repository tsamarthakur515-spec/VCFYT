FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies + Node.js
RUN apt-get update && \
    apt-get install -y \
        curl \
        git \
        build-essential \
        ffmpeg \
        libopus0 \
        libopus-dev \
        libmp3lame0 \
        libx264-160 \
        python3-dev \
        libffi-dev \
        libssl-dev \
        aria2 \
        ca-certificates \
        wget \
        gnupg \
        lsb-release && \
    # Install Node.js 18
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create downloads folder
RUN mkdir -p /app/downloads

# Run bot
CMD ["python", "main.py"]
