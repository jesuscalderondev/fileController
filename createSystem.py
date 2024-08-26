import shutil
import os

if os.path.exists("backup"):
    # Elimina la carpeta y todos sus contenidos
    shutil.rmtree("backup")
    print(f"La carpeta ha sido eliminada")
else:
    print(f"La carpeta backup no existe")
    

if os.path.exists("files"):
    # Elimina la carpeta y todos sus contenidos
    shutil.rmtree("files")
    print(f"La carpeta files ha sido eliminada")
else:
    print(f"La carpeta files no existe")
    

if os.path.exists("database.sqlite"):
    # Elimina la carpeta y todos sus contenidos
    os.remove("database.sqlite")
else:
    print(f"La carpeta database no existe")