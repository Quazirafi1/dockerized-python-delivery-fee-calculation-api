FROM python:3.9

# Install dependencies from requirements.txt
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the rest of your application code
COPY . /app

# Set the working directory to /app
WORKDIR /app

# The command to run your application
CMD ["python", "./main.py"]
