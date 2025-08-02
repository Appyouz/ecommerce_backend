# base image start from an official python package
FROM python:3.12-slim
# Declare build arguments (these are passed from render.yaml)
ARG SECRET_KEY
ARG DATABASE_URL
ARG DEBUG_BUILD # Using DEBUG_BUILD to avoid direct conflict if you have a runtime DEBUG var
ARG DJANGO_ALLOWED_HOSTS
ARG DJANGO_CORS_ALLOWED_ORIGINS
ARG DJANGO_CSRF_TRUSTED_ORIGINS
ARG DJANGO_ENV
ARG CLOUDINARY_URL

# Set environment variables from build arguments
# These ENV vars will be available to RUN commands during build (like collectstatic)
# and also to the CMD (your gunicorn server) at runtime.
ENV SECRET_KEY=$SECRET_KEY
ENV DATABASE_URL=$DATABASE_URL
ENV DEBUG=$DEBUG_BUILD
ENV DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS 
ENV DJANGO_CORS_ALLOWED_ORIGINS=$DJANGO_CORS_ALLOWED_ORIGINS
ENV DJANGO_CSRF_TRUSTED_ORIGINS=$DJANGO_CSRF_TRUSTED_ORIGINS
ENV DJANGO_ENV=${DJANGO_ENV}
ENV CLOUDINARY_URL=$CLOUDINARY_URL

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


# Expose port
EXPOSE 8000

# Define the command to run the application using Gunicorn
# Using python -m for robustness
CMD python manage.py migrate --noinput && \
    DJANGO_ENV=production python -m gunicorn ecommerce_backend.wsgi:application --bind 0.0.0.0:$PORT
