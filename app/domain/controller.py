from abstracts.controller import Service
from app.domain.models import model, File, User, Permission, Dependence, Clasification
from flask import session as cookies
from abstracts.objects import Json
from sqlalchemy.exc import IntegrityError
import os

class appServices(Service):

    session = model.Session
    model.createBase()

    #creation

    def registerNewUser(self, json, admin=False):
        try:
            if admin:
                json.add("admin", admin)

            newUser = User(json)
            self.session.add(newUser)
            self.session.commit()

            return "Usuario registrado de manera exitosa"
        except Exception as e:
            self.session.rollback()
            if isinstance(e, IntegrityError):
                raise Exception("Uno de los datos proporcionados ya pertenece a un usuario, por favor, verificar la información.")
            raise Exception(f"No se pudo guardar el usuario, esto puede deberse a algún error de conexión o perdida de datos {e}")

    def registerNewFile(self, json, file:any=None):
        try:
            newFile = File(json)
            self.session.add(newFile)
            self.session.commit()

            if file is not None:
                dependence = self.session.get(Dependence, newFile.dependenceId)
                clasification = self.session.get(Clasification, newFile.clasificationId)
                route = f"files/{dependence.directory}/{dependence.acronym}-{clasification.acronym}-{newFile.num}-{newFile.secureName}.{newFile.extension}"
                file.save(route)

            return "El archivo fue guardado de forma exitosa"
        except Exception as e:
            self.session.rollback()
            if isinstance(e, IntegrityError):
                raise Exception("Este archivo ya existe, si desea modificarlo, vaya a la opción de busqueda.")
        raise Exception("Algo ha fallado, revisa tu conexión e intenta de nuevo")

    def registerDependence(self, json:Json):
        try:
            newDependence = Dependence(json)
            self.session.add(newDependence)
            self.session.commit()

            os.mkdir(f"files/{newDependence.directory}")

            return "Área creada de manera exitosa"
        except Exception as e:
            self.session.rollback()
            if isinstance(e, IntegrityError):
                raise Exception("Esta área ya existe")