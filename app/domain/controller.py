from abstracts.controller import Service
from app.domain.models import model, File, User, Permission, Dependence, Clasification, Log, Request, Notification
from flask import session as cookies
from abstracts.objects import Json, ExcelGenerator
from sqlalchemy.exc import IntegrityError
import os
import traceback
from functools import wraps
from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode
from flask import render_template, send_file
from uuid import UUID
from extensions import getBackUp, getWorkSpace
from werkzeug.datastructures import FileStorage
import traceback
import shutil

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
            
            newFile.extension = file.filename.split('.')[-1]
            num = self.session.query(File).filter(File.dependenceId == newFile.dependenceId, File.clasificationId == newFile.clasificationId).order_by(File.num.asc()).first()
            newFile.secureName = self.createSecureName(newFile.name)
            num = (num.num if num != None else 0) + 1
            
            print(num, "Este es el numero")
            newFile.num = num
            dependence = self.session.get(Dependence, newFile.dependenceId)
            clasification = self.session.get(Clasification, newFile.clasificationId)
            route = f"{dependence.directory}/{clasification.acronym}-{dependence.acronym}-{self.getNum(num)}-{newFile.secureName}.{newFile.extension}"
            newFile.route = route
            self.session.add(newFile)
            self.session.commit()
            self.registerLog("Creación", newFile.id)
            file.filename = f"{clasification.acronym}-{dependence.acronym}-{self.getNum(num)}-{newFile.secureName}.{newFile.extension}"
            file.save(f"{getWorkSpace()}{route}")
            file.seek(0)
            file.save(f"{getBackUp()}{route}")

            return "El archivo fue guardado de forma exitosa"
        except Exception as e:
            print(traceback.format_exc())
            
            self.session.rollback()
            if isinstance(e, IntegrityError):
                raise Exception("Este archivo ya existe, si desea modificarlo, vaya a la opción de busqueda.")
            raise Exception("Algo ha fallado, revisa tu conexión e intenta de nuevo")

    def registerDependence(self, json:Json):
        try:
            newDependence = Dependence(json)
            self.session.add(newDependence)
            self.session.commit()

            os.mkdir(f"{getWorkSpace()}{newDependence.directory}")
            os.mkdir(f"{getBackUp()}{newDependence.directory}")

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
    
    
    #Oters
    
    def login(self, email:str, password:str):
        try:
            user = self.session.query(User).filter(User.email == email).first()
            print(self.passwordVerify(user.password, password))
            if self.passwordVerify(user.password, password):
                token = self.creatreJWT(user.id)
                cookies["token"] = token
                return token
        except Exception as e:
            print(traceback.print_exception(e))
            raise Exception("Correo o contraseña incorrecto")
        
    
    def adminRequired(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):

            if 'token' in cookies:
                token = cookies["token"]

                if not token:
                    return render_template("withOutSession.html")

                try:
                    payload = decode(token, os.environ.get("SECRET_KEY"), algorithms=['HS256'])
                    user = self.session.get(User, UUID(payload.get("id")))
                    depence = self.session.get(Dependence, user.dependenceId)
                    
                    
                    if not user.admin or depence.acronym != "CIN":
                        raise ExpiredSignatureError()
                except (ExpiredSignatureError, InvalidTokenError) as e:
                    if isinstance(e, ExpiredSignatureError):
                        return "No eres administrador"
                    elif isinstance(e, InvalidTokenError):
                        return render_template("invalidSession.html")
                return f(*args, **kwargs)
            return render_template("withOutSession.html")

        return decorated
    
        
    def deleteFile(self, id:UUID):
        try:
            
            
            fileObj = self.session.get(File, id)
            os.remove(f"{getWorkSpace()}{fileObj.route}")
            fileObj.view = False
            self.session.add(fileObj)
            self.session.commit()
            self.registerLog("Eliminar", id)
            return "Se ha eliminado el documento, requerde que esto no es de forma total y que existe el backup"
        except Exception as e:
            self.session.rollback()
            print(traceback.format_exc())
            raise Exception("Al parecer este archivo ya no existe, refresque la página.")
    
    #Gets
    
    def getFiles(self, view=True):
        try:
            
            files = []
            filesResponse = []
            userId = self.getUser()
            user = self.session.get(User, userId)
            dependence = self.session.get(Dependence, user.dependenceId)
            
            print(user.admin)
            
            if not user.admin or (user.admin and dependence.acronym != "CIN"):
                
                
                files.extend(dependence.files)
                
                for permission in user.permissions:
                    if permission.fileId is not None:
                        archive = self.session.get(File, permission.fileId)
                        if archive not in files:
                            files.append(archive)
                
                for archive in files:
                    if archive.view == view:
                        filesResponse.append(
                            {
                                "id": archive.id,
                                "name": archive.route.split("/")[-1],
                                "edit" : False,
                                "extension" : archive.extension,
                                "delete" : False,
                                "download" : True,
                                "see" : True if archive.extension == "pdf" else False
                            }
                        )
            else:
                files = self.session.query(File).filter(File.view == view).all()
                print(files)
            
            
                for archive in files:

                    filesResponse.append(
                        {
                            "id": archive.id,
                            "name": archive.route.split("/")[-1],
                            "extension" : archive.extension,
                            "edit" : True,
                            "delete" : True,
                            "download" : True,
                            "see" : True if archive.extension == "pdf" else False
                        }
                    )
            return filesResponse
        except Exception as e:
            print(traceback.format_exc())
            raise Exception("No hay archivos que mostrar")
    

    def getClasifications(self):
        try:
            response = []
            clasifications = self.session.query(Clasification).all()
            for clasification in clasifications:
                response.append(
                    {
                        "id" : clasification.id,
                        "name" : clasification.name
                    }
                )
            return response
        except:
            raise Exception("Se perdió la conexión")
        
    def getDepencencies(self):
        try:
            response = []
            dependencies = self.session.query(Dependence).all()
            for dependence in dependencies:
                response.append(
                    {
                        "id" : dependence.id,
                        "name" : dependence.name
                    }
                )
            return response
        except:
            raise Exception("Se perdió la conexión")
        
    def registerLog(self, action:str, fileId:UUID=None):
        json = Json(
            {
                "action" : action,
                "userId" : self.getUser(),
                "fileId" : fileId
            }
        )
        newLog = Log(json)
        self.session.add(newLog)
        self.session.commit()
        
    def getDocument(self, id:UUID, state:int):
        file = self.session.get(File, id)
        if state in [0, 1]:
            self.registerLog("Descarga" if state == 1 else "Ver", id)
            
            path = f"{getWorkSpace()}{file.route}"
        elif state == 2:
            path = f"{getBackUp()}{file.route}"
        return send_file(path_or_file=path, as_attachment=state in [2, 1])
    
    def getDocumentWithDirectory(self, directory:str, name:str):
        file = self.session.query(File).filter(File.route == f"{directory}/{name}").first()
        if(file != None):
            self.registerLog("Descarga", file.id)
        return send_file(path_or_file=f"{getWorkSpace()}{directory}/{name}", as_attachment=True)
    
    def getBackup(self, id:UUID, download=False):
        self.registerLog("Descarga" if download else "Ver", id)
        file = self.session.get(File, id)
        return send_file(path_or_file=f"{getBackUp()}{file.route}", as_attachment=download)

    def getPermissions(self):
        try:
            
            
            user = self.session.get(User, self.getUser())
            dependence = self.session.get(Dependence, user.dependenceId)
            
            
            response = {
                "admin" : user.admin and dependence.acronym != "CIN",
                "create" :  user.admin and dependence.acronym == "CIN",
                "chatIA" : user.admin or dependence.acronym != "CIN"
            }
            
            return response
        except Exception as e:
            print(traceback.format_exc())
            raise Exception("Se perdió la conexión")
        
    def getNotifications(self):
        try:
            user = self.session.get(User, self.getUser())
            
            
            notifications = self.session.query(Notification).filter(Notification.recept == user.id).all()
            response = {"linked" : user.dependenceId == self.session.query(Dependence).filter(Dependence.acronym == "CIN").first().id}
            
            notifys = []

            for notify in notifications:
                notifys.append({
                    "description" : notify.description,
                    "id" : notify.permission if notify.permission != None else notify.requestId
                })
            
            response["notifications"] = notifys
            
            return response
        except Exception as e:
            print(traceback.format_exc())
            raise Exception("Algo ha pasado")
        
            
            
    def getLogs(self):
        try:
            logs = self.session.query(Log).all()
            
            response = []
            
            for log in logs:
                
                user = self.session.get(User, log.userId)
                if log.fileId != None:
                    archive = self.session.get(File, log.fileId)
                    name = archive.route.split("/")[-1]
                    extension = archive.extension
                else:
                    name = "Archivo no subido"
                    extension = "Sin extensión"
                response.append({
                    "extension" : extension,
                    "name" :  f"{name} - Usuario: {user.names}",
                    "date" : self.getDateString(log.createAt),
                    "action" : log.action
                })
            return response
        except Exception as e:
            print(traceback.format_exc())
            raise Exception("No se pudo obtener el Log")
        
        
    def registerRequest(self, json:Json, file=None):
        try:
            json.add(json.action, True)
            newRequest = Request(json)
            try:
                newRequest.newClasification = UUID(newRequest.newClasification)
                newRequest.newDependence = UUID(newRequest.newDependence)
            except:
                pass
            userId = self.getUser()
            newRequest.userId = userId
            user = self.session.get(User, userId)
            
            recipient = self.session.query(User).filter(User.dependenceId == self.session.query(Dependence).filter(Dependence.acronym == "CIN").first().id).first()
            
            if file.filename != "":
                extension = file.filename.split('.')[-1]
                newRequest.nameFile = self.createSecureName(newRequest.nameFile)
                newRequest.routeFileRequest = f"requests/{newRequest.nameFile}.{extension}"
                file.save(f"{getWorkSpace()}{newRequest.routeFileRequest}")
                
                
            actions = {
                "edit2" : "Reclasificación / cambio de código",
                "edit" : "Modificación",
                "delete" : "Eliminación",
                "create" : "Creación"
            }
            
            permission = actions[json.action]
            
            jsonNotify = Json({
                "recept" : recipient.id,
                "emit" : userId,
                "requestId" : newRequest.id,
                "description" : f"{user.names} ha realizado una solicitud de {permission}"
            })
            
            newNotify = Notification(jsonNotify)
            self.session.add_all([newRequest, newNotify])
            
            
            self.mail.sendMail({
                "subject": "Nueva solicitud de permiso",
                "body": f"Se ha creado una nueva solicitud por el usuario {user.names}. Para más información ingrese al sistema AI-rchive para conocer los detalles",
                "recipients": [recipient.email]
            })
            
            archive = self.session.query(File).filter(File.clasificationId == newRequest.clasificationId, File.dependenceId == newRequest.dependenceId, File.secureName == newRequest.nameFile).first()
            if archive != None:
                self.registerLog("Solicitud de cambio", archive.id)
            else:
                self.registerLog("Solicitud de creación", None)
            self.session.commit()
            return "Su solicitud fue enviada, aguarda a la espera de una respuesta"
        except Exception as e:
            print(traceback.format_exc())
            self.session.rollback()
            raise Exception("No se puedo guardar")

    def getDetailsRequest(self, id:UUID):
        try:
            request = self.session.get(Request, id)
            
            actions = {
                "edit2" : "Reclasificación / cambio de código",
                "edit" : "Modificación",
                "delete" : "Eliminación",
                "create" : "Creación"
            }
            
            permissions = [request.edit2, request.edit, request.delete ,request.create]
            permission = actions[list(actions.keys())[permissions.index(True)]]
            
            dependence = self.session.get(Dependence, request.dependenceId)
            clasification = self.session.get(Clasification, request.clasificationId)
            
            data = {
                "description" : request.description,
                "permission" : permission,
                "name" : f"{clasification.acronym}-{dependence.acronym}-xxx-{request.nameFile}",
                "emails" : request.emails,
                "nameOld" : "No"
            }
                
            if request.routeFileRequest != None:
                data["name"] += "." + request.routeFileRequest.split(".")[-1]
                data["route"] = request.routeFileRequest
            
            if request.newClasification != None or request.newDependence != None:
                dependenceN = self.session.get(Dependence, request.newDependence)
                clasificationN = self.session.get(Clasification, request.newClasification)
                data["name"] = f"{clasificationN.acronym}-{dependenceN.acronym}-xxx-{request.nameFile}"+request.routeFileRequest.split(".")[-1]
            
                
            archive = self.session.query(File).filter(File.dependenceId == dependence.id, File.clasificationId == clasification.id, File.secureName == request.nameFile).first()
            print(archive, "Archiveee")
            if archive != None:
                data["routeOld"] = archive.route
                data["nameOld"] = archive.route.split("/")[-1]
            
            return data
        except:
            print(traceback.format_exc())
            Exception("Algo ha pasado")

    def responseRequest(self, json:Json, file=None):
        try:
            
            myRequest = self.session.get(Request, UUID(json.requestId))
            userRe = self.session.get(User, self.getUser())
            creatorRequest = self.session.get(User, myRequest.userId)
            
            newNotifY = Notification(Json({
                "description" : "",
                "requestId" : None,
                "permission" : None,
                "recept" : creatorRequest.id,
                "emit" : userRe.id
            }))
            
            if(json.action == "accept"):
                dependence = self.session.get(Dependence, myRequest.dependenceId)
                clasification = self.session.get(Clasification, myRequest.clasificationId)
                archive = self.session.query(File).filter(File.dependenceId == dependence.id, File.clasificationId == clasification.id, File.secureName == myRequest.nameFile).first()
                
                if myRequest.create == False:
                    
                    if myRequest.delete:
                        archive.view = False
                        self.session.add(archive)
                        self.session.commit()
                        os.remove(f"{getWorkSpace()}{archive.route}")
                        self.registerLog("Eliminar", archive.id)
                        newNotifY.description = f"Se ha aprovado tu solicitud de creación referente al archivo {myRequest.nameFile}"
                        self.mail.sendMail({
                            "subject": "Solicitud reachazada",
                            "body": f"Se ha aprovado tu solicitud de creación referente al archivo {myRequest.nameFile} y se realizaron las adecuaciones necesarias, algunos detalles: {json.details}",
                            "recipients": self.getMails(myRequest.emails)
                        }, archive=file)
                    
                    if myRequest.edit:
                        file.save(f"{getWorkSpace()}{archive.route}")
                        file.seek(0)
                        self.registerLog("Edición", archive.id)
                        
                        file.seek(0)
                        file.filename = archive.route.split("/")[-1]
                        newNotifY.description = f"Se ha aprovado tu solicitud de modificación referente al archivo {myRequest.nameFile}"
                        self.mail.sendMail({
                            "subject": "Solicitud reachazada",
                            "body": f"Se ha aprovado tu solicitud de modificación referente al archivo {myRequest.nameFile} y se realizaron las adecuaciones necesarias, algunos detalles: {json.details}",
                            "recipients": self.getMails(myRequest.emails)
                        }, archive=file)
                        
                    if myRequest.edit2:
                        
                        ruteOld = f"{getWorkSpace()}{archive.route}"
                        
                        
                        dependence = self.session.get(Dependence, myRequest.newDependence)
                        clasification = self.session.get(Clasification, myRequest.newClasification)
                        
                        archive.dependenceId = dependence.id
                        archive.clasificationId = clasification.id
                        num = self.session.query(File).filter(File.dependenceId == dependence.id, File.clasificationId == clasification.id).order_by(File.num.asc()).first()
                        archive.extension = file.filename.split('.')[-1]
                        archive.routeOld = ruteOld
                        archive.route = f"{dependence.directory}/{clasification.acronym}-{dependence.acronym}-{self.getNum(num.num)}-{myRequest.nameFile}.{archive.extension}"
                        self.session.add(archive)
                        self.session.commit()
                        file.save(f"{getWorkSpace()}{archive.route}")
                        file.seek(0)
                        file.save(f"{getBackUp()}{archive.route}")
                        self.registerLog("Reclasificación", archive.id)
                        os.remove(ruteOld)
                        
                        file.seek(0)
                        file.filename = archive.route.split("/")[-1]
                        newNotifY.description = f"Se ha aprovado tu solicitud de reclasificación referente al archivo {myRequest.nameFile}"
                        self.mail.sendMail({
                            "subject": "Solicitud aprovada",
                            "body": f"Se ha aprovado tu solicitud de reclasificación referente al archivo {myRequest.nameFile} y se realizaron las adecuaciones necesarias, algunos detalles: {json.details}",
                            "recipients": self.getMails(myRequest.emails)
                        }, archive=file)
                        
                else:
                    self.registerFile(Json({
                        "name" : myRequest.routeFileRequest.split("/")[-1].split(".")[0],
                        "dependenceId" : myRequest.dependenceId,
                        "clasificationId" : myRequest.clasificationId
                    }), file)
                    
                    archive = self.session.query(File).filter(File.dependenceId == dependence.id, File.clasificationId == clasification.id, File.secureName == myRequest.nameFile).first()
                    print(archive, "************************************************")
                    file.seek(0)
                    file.filename = archive.route.split("/")[-1]
                    newNotifY.description = f"Se ha aceptado tu solicitud de creación referente al archivo {myRequest.nameFile}"
                    
                    try:
                        self.mail.sendMail({
                            "subject": "Solicitud reachazada",
                            "body": f"Se ha aprovado tu solicitud de creación referente al archivo {myRequest.nameFile} y se realizaron las adecuaciones necesarias, algunos detalles: {json.details}",
                            "recipients": self.getMails(myRequest.emails)
                        }, archive=file)
                    except:
                        pass
                
            else:
                newNotifY.description = f"Se ha reachazado tu solicitud de creación referente al archivo {myRequest.nameFile}"
                
                self.mail.sendMail({
                    "subject": "Solicitud reachazada",
                    "body": f"Se ha rechazado tu solicitud referente al archivo {myRequest.nameFile}, estas fueron alguas de las observaciones {json.details}",
                    "recipients": [creatorRequest.email]
                })
            if myRequest.routeFileRequest != None:
                os.remove(f"{getWorkSpace()}{myRequest.routeFileRequest}")
                
            oldNotify = self.session.query(Notification).filter(Notification.requestId == myRequest.id).first()
            self.session.delete(oldNotify)
            self.session.delete(myRequest)
            self.session.commit()
            return "Se han realizado y guardado los cambios pertinentes"
        except Exception as e:
            print(traceback.format_exc())
            self.session.rollback()
            raise Exception("Algo salió mal")
        
    def backArchive(self, fileId:UUID):
        try:
            file = self.session.get(File, fileId)
            file.view = True
            shutil.copy(f"{getBackUp()}{file.route}", f"{getWorkSpace()}{file.route}")
            self.session.add(file)
            self.session.commit()
            self.registerLog("Restauración", file.id)
            return "El archivo fue restaurado a su versión anterior"
        except:
            print(traceback.format_exc())
            raise Exception("No se puedo volver a la versíon anterior")
        
    def downloadHistory(self):
        generator = ExcelGenerator(self.getLogs())
        return send_file(generator.generate(), as_attachment=True)