# base image start from an official python package
FROM python:3.11-slim-buster

# Set Environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1 

# Set working directory
WORKDIR /app

COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r ./requirements.txt gunicorn

# Copy application code
COPY . /app/


# Collect static files into STATIC_ROOT
# This needs to run AFTER copying all your application code
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Define the command to run the application
# This command starts the Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "ecommerce_backend.wsgi:application", "--bind", "0.0.0.0:${PORT:-8000}"]

