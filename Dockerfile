FROM python:3.9-alpine

WORKDIR /app

# Zero dependencies, so we just copy the core files
COPY server.py index.html ./
# Create configs directory
RUN mkdir -p /app/configs

# Expose the API and UI port
EXPOSE 5000

# Set environment variables for docker to optimize python runs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "server.py"]
