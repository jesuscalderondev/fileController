title Flask Server
echo "Se esta empezando a ejecutar el servidor"

echo "descargando el entorno virtual"
python pip install virtualenv

echo "creando el entorno virtual"
virtualenv env

echo "activando el entorno virtual"
call .\env\Scripts\activate

echo "instalando las dependencias"
:: Instalar dependencias (si es necesario)
pip install -r requirements.txt

rmdir files/
rmdir backup/
del databa

echo "ejecutando el programa"
:: Ejecutar aplicación Python

python createSystem.py

python server.py

pause