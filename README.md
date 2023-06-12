# Api Write Wise 

Este proyecto fue creado para interactuar con chatgpt 3.5 y recuperar la respuesta para generar reportes enfocados en el desarrollo del crecimiento del niñ@ en un jardin infantil.
Esta api corre en un servicio google cloud,como un archivo docker alojado en container registry y corriendo en google run.
Cuenta con un sistema de logueo y registro de usuarios, para poder acceder a la api y generar reportes, la base de datos usado es mongodb atlas. 
En resumen la api hace uso de las siguientes librerias y/o servicios:
* Chatgpt 3.5
* Google cloud: container Registry, gogle run
* Mongodb atlas
* Django
* Django rest framework

## Run app localmente
Para ejecutar el proyecto se debe crear un entorno virtual venv y activarlo, luego instalar las dependencias necesarias para correr la app, y por ultimo correr la app en modo desarrollo.

### `python -m venv writeWise-env`
crea un entorno virtual llamado writeWise-env

### `source writeWise-env/bin/activate`
activa el entorno virtual

en la carpeta del entorno virtual copiar el folder api_write. Luego, dentro de api_write ejecutar los siguientes comandos:

### `pip install`
instalar las dependencias necesarias para correr la app

### `python manage.py runserver`
correra la app en modo desarrollo.\
Abrir [http://localhost:8080](http://localhost:8080).


## Run google cloud
En el directorio del proyecto, donde se encuentre el archivo Dockerfile, puedes correr: 

### `docker build -t api_writewise:Vx.x .`
crea un docker con del proyecto asignar la version del archivo docker

### `docker tag api_writewise:VX.X  gcr.io/utopian-button-382400/api_writewise:VX.X` 
crea una etiqueta para versionar y organizar las imágenes de la api

### `docker push  gcr.io/<id_proyecto_google_cloud>/api_writewise:VX.X`
sube el archivo docker al servicio container registre

cuando el archivo docker se haya subido, desde el servicion de google run se selecciona este docker y se ejecuta
