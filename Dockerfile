FROM python:3.12.3-slim

ENV APP_HOME /app

# Upgrade pip
RUN pip install --upgrade pip

# Set working directory
WORKDIR $APP_HOME

# Copy project files
COPY . ./

# Install Python dependencies
RUN pip install -r requirements.txt

# Define default command
CMD ["python", "app.py"]