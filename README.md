# Proyecto

## Correr con Python

1. Clona este repositorio en tu computador.

2. Crea un archivo `.env` en la raíz del proyecto (con los valores correspondientes al analizador de imágenes):

```
IP_SERVER=YOUR_IP_SERVER
API_KEY=YOUR_API_KEY
```

3. Ejecuta el siguiente comando `python manage.py runserver`

## Correr con Docker

1. Clona este repositorio en tu computador.

2. Ejecuta el siguiente comando para construir la imagen, ubicado en la raíz del proyecto.

`sudo docker build --build-arg API_KEY=YOUR_API_KEY --build-arg IP_SERVER=YOUR_IP_SERVER -t django-app .`

3. Ejecuta el siguiente comando correr el proyecto en localhost.

`sudo docker container run -d --name django-docker -p 80:80 django-app`

## Correr con Docker Hub

1. Ejecuta el siguiente comando correr el proyecto en localhost.

`sudo docker run -d -p 80:80 --name sasvar danielgara/sasvar`
