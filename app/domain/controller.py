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

    def registerUser(self, json:Json):
        try:

            newUser = User(json)
            self.session.add(newUser)
            self.session.commit()

            return "Usuario registrado de manera exitosa"
        except Exception as e:
            self.session.rollback()
            if isinstance(e, IntegrityError):
                raise Exception("Uno de los datos proporcionados ya pertenece a un usuario, por favor, verificar la información.")
            raise Exception(f"No se pudo guardar el usuario, esto puede deberse a algún error de conexión o perdida de datos {e}")

    def registerFile(self, json, file:any=None):
        try:
            
            
            newFile = File(json)
            num = self.session.query(File).filter(File.dependenceId == newFile.dependenceId, File.clasificationId == newFile.clasificationId).order_by(File.num.asc()).first()
            
            num = (num if num != None else 0) + 1
            newFile.num = num
            dependence = self.session.get(Dependence, newFile.dependenceId)
            clasification = self.session.get(Clasification, newFile.clasificationId)
            route = f"files/{dependence.directory}/{clasification.acronym}-{dependence.acronym}-{self.getNum(num)}-{newFile.secureName}.{newFile.extension}"
            newFile.route = route
            self.session.add(newFile)
            self.session.commit()

            if file is not None:
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
            raise Exception(f"No se pudo guardar la dependencia, esto puede deberse a algún error de perdida de datos.\nDetalles tecnico: {e}")
            
    def registerClasification(self, json:Json):
        try:
            
            newClasification = Clasification(json)
            self.session.add(newClasification)
            self.session.commit()
            return "El tipo de documento fue creado exitosamente"
        except Exception as e:
            self.session.rollback()
            if isinstance(e, IntegrityError):
                raise Exception("Este tipo de documento ya existe")
            raise Exception(f"No se pudo guardar, esto puede deberse a algún error de perdida de datos.\nDetalles tecnico: {e}")
    
    