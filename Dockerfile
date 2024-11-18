# Use the latest lightweight version of Python
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir telethon
RUN pip install --no-cache-dir googletrans==4.0.0-rc1

# Run the bot script
CMD ["python", "telegram-forwarding-bot.py"]
