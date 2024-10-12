# Use Python 3.10 as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt /app/

# Install dependencies
RUN pip3 install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Define the command to run the bot
CMD ["python3", "bot.py"]
