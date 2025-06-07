# base image start from an official python package
FROM python:3.11-slim-buster

# Declare build arguments (these are passed from render.yaml)
ARG SECRET_KEY
ARG DATABASE_URL
ARG DEBUG_BUILD # Using DEBUG_BUILD to avoid direct conflict if you have a runtime DEBUG var
ARG DJANGO_ALLOWED_HOSTS

# Set environment variables from build arguments
# These ENV vars will be available to RUN commands during build (like collectstatic)
# and also to the CMD (your gunicorn server) at runtime.
ENV SECRET_KEY=$SECRET_KEY
ENV DATABASE_URL=$DATABASE_URL
ENV DEBUG=$DEBUG_BUILD
ENV DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS 

# Set other environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker's caching
COPY requirements.txt ./

# Install production dependencies
RUN pip install --no-cache-dir -r ./requirements.txt gunicorn

# Copy application code
COPY . /app/

# Collect static files into STATIC_ROOT
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Define the command to run the application using Gunicorn
# Using python -m for robustness
# CMD ["python", "-m", "gunicorn", "ecommerce_backend.wsgi:application", "--bind", "0.0.0.0:${PORT:-8000}"]
CMD python manage.py migrate --noinput && python -m gunicorn ecommerce_backend.wsgi:application --bind 0.0.0.0:${PORT:-8000}
