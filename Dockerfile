# Use an official Python runtime as a parent image
FROM python:3.12

ARG API_KEY
ENV API_KEY=$API_KEY
ARG IP_SERVER
ENV IP_SERVER=$IP_SERVER
ARG CRYPTO_KEY
ENV CRYPTO_KEY=$CRYPTO_KEY
ARG EMAIL_HOST_USER
ENV EMAIL_HOST_USER=$EMAIL_HOST_USER
ARG EMAIL_HOST_PASSWORD
ENV EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port the Django app runs on
EXPOSE 8000

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]