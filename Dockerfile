FROM python:3.10-slim-buster

WORKDIR /app

# Copy requirements and install python packages plus awscli via pip
# This avoids unreliable Debian apt mirrors and keeps the build incredibly fast and robust!
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt awscli

# Copy all source files
COPY . .

# Install the local package in editable mode now that setup.py and code are copied
RUN pip install -e .

CMD ["python3", "app.py"]
