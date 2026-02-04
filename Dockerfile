# MCP server template - Python
FROM python:3.12.2-slim

WORKDIR /app

# Upgrade pip first
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy server code and examples
COPY server/ ./server/
COPY examples/ ./examples/

# Optional: Copy environment config if needed
# COPY .env ./

# Expose port (documentation)
EXPOSE 8000

# Default environment variable
ENV PORT=${PORT:-8000}

# Start MCP server
CMD ["python", "-m", "server.main"]
