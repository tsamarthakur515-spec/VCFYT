# ───────────────────────────────────────────────
# Use Python 3.10 slim as base image
# ───────────────────────────────────────────────
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose optional port (not required for Telegram)
EXPOSE 8080

# Set environment variable for Pyrogram session (optional)
# You can override this at runtime with: -e SESSION_STRING="..."
# ENV SESSION_STRING="YOUR_STRING_SESSION_HERE"

# Run main.py
CMD ["python", "main.py"]
