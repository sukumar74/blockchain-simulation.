# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all files from your project into the container
COPY . .

# Install dependencies (if any)
RUN pip install --no-cache-dir -r requirements.txt || true

# Run the blockchain simulation script
CMD ["python", "blockchain.py"]
