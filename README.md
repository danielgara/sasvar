# Proyecto

## Correr con Python

1. Clona este repositorio en tu computador.

2. Crea un archivo `.env` en la raíz del proyecto (con los valores correspondientes al analizador de imágenes):

```
IP_SERVER=YOUR_IP_SERVER
API_KEY=YOUR_API_KEY
CRYPTO_KEY=YOUR_CRYPTO_KEY
EMAIL_HOST_USER=YOUR_EMAIL_HOST_USER
EMAIL_HOST_PASSWORD=YOUR_EMAIL_HOST_PASSWORD
```

3. Ejecuta el siguiente comando `python manage.py runserver`

## Correr con Docker

1. Clona este repositorio en tu computador.

2. Ejecuta el siguiente comando para construir la imagen, ubicado en la raíz del proyecto.

`sudo docker build --build-arg API_KEY=YOUR_API_KEY --build-arg IP_SERVER=YOUR_IP_SERVER --build-arg CRYPTO_KEY=YOUR_CRYPTO_KEY --build-arg EMAIL_HOST_USER=YOUR_EMAIL_HOST_USER --build-arg EMAIL_HOST_PASSWORD=YOUR_EMAIL_HOST_PASSWORD -t django-app .`

3. Ejecuta el siguiente comando correr el proyecto en localhost.

`sudo docker container run -d --name django-docker -p 80:80 django-app`

## Correr con Docker Hub

1. Ejecuta el siguiente comando correr el proyecto en localhost.

`sudo docker run -d -p 8000:8000 --name sasvar danielgara/sasvar`

## Correr con Docker Hub y Volumenes (persistir datos de DB)

1. Crea un par de volumenes 

`sudo docker volume create sasvardb`
`sudo docker volume create sasvarpics`

2. Ejecuta el siguiente comando correr el proyecto en localhost.

`sudo docker run -v sasvardb:/code/db -v sasvarpics:/code/uploads -d -p 8000:8000 --name sasvar danielgara/sasvar`

