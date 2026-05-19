FROM python:3.10-slim-buster
WORKDIR /app

# Install system dependencies & awscli in a single consolidated layer
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends awscli && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install python packages (with no-cache-dir to keep image small)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . .

CMD ["python3", "app.py"]
