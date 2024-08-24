from abstracts.controller import Service
from app.domain.models import model, File, User, Permission, Dependence, Clasification, Log, Request, Notification
from flask import session as cookies
from abstracts.objects import Json
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
            
            self.registerLog("Create", newFile.id)
            file.save(f"{getWorkSpace()}{route}")
            file.save(f"{getBackUp()}{route}")

            return "El archivo fue guardado de forma exitosa"
        except Exception as e:
            print(e)
            
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
    
    def registerRequest(self, json:Json, file=None):
        try:
            json.add(json.action, True)
            newRequest = Request(json)
            userId = self.getUser()
            newRequest.userId = userId
            user = self.session.get(User, userId)
            
            
            
            
            recipient = self.session.query(User).filter(User.dependenceId == self.session.query(Dependence).filter(Dependence.acronym == "CIN").first().id).first()
            
            if file.filename != "":
                extension = file.filename.split('.')[-1]
                newRequest.nameFile = self.createSecureName(newRequest.nameFile)
                newRequest.routeFileRequest = f"requests/{newRequest.nameFile}.{extension}"
                file.save(f"{getWorkSpace()}{newRequest.routeFileRequest}")
            
            jsonNotify = Json({
                "recept" : recipient.id,
                "emit" : userId,
                "requestId" : newRequest.id,
                "description" : f"{user.names} ha realizado una solicitud"
            })
            
            newNotify = Notification(jsonNotify)
            self.session.add_all([newRequest, newNotify])
            self.session.commit()
            
            self.mail.sendMail({
                "subject": "Nueva solicitud de permiso",
                "body": f"Se ha creado una nueva solicitud de permiso para el usuario {user.names}. Para más información ingrese al sistema AI-rchive para conocer los detalles",
                "recipients": [recipient.email]
            })
            
            return "Su solicitud fue enviada, aguarda a la espera de una respuesta"
        except Exception as e:
            print(e)
            self.session.rollback()
            raise Exception("No se puedo guardar")
    
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
                    
                    
                    
                    if not user.admin:
                        raise ExpiredSignatureError()
                except (ExpiredSignatureError, InvalidTokenError) as e:
                    if isinstance(e, ExpiredSignatureError):
                        return "No eres administrador"
                    elif isinstance(e, InvalidTokenError):
                        return render_template("invalidSession.html")
                return f(*args, **kwargs)
            return render_template("withOutSession.html")

        return decorated
    
    def responseRequest(self, json:Json):
        try:
            myRequest = self.session.get(Request, UUID(json.requestId))
            depend = self.session.get(Dependence, myRequest.dependenceId)
            clasifi = self.session.get(Clasification, myRequest.clasificationId)
            userRe = self.session.get(User, self.getUser())
            
            newNotifY = Notification(Json({
                "description" : "",
                "requestId" : None,
                "permission" : None,
                "recept" : myRequest.userId,
                "emit" : userRe.id
            }))
            
            file = None
            
            data = None
            
            if(json.action == "accept"):
                
                if(myRequest.edit or myRequest.edit2 or myRequest.create or myRequest.download):
                    
                    if myRequest.edit or myRequest.edit2 or myRequest.create:
                        
                        
                        archive = open(f"{getWorkSpace()}{myRequest.routeFileRequest}", "rb")
                        file = FileStorage(archive, filename=myRequest.routeFileRequest.split("/")[-1])
                    
                        self.registerFile(Json({
                            "name" : myRequest.routeFileRequest.split("/")[-1].split(".")[0],
                            "dependenceId" : myRequest.dependenceId,
                            "clasificationId" : myRequest.clasificationId
                        }), file)
                        
                        idFile = self.session.query(File).filter(File.secureName == myRequest.routeFileRequest.split("/")[-1].split(".")[0]).first().id
                        
                        newPermission = Permission(Json({
                            "userId" : myRequest.userId,
                            "fileId" : idFile,
                            "edit" : myRequest.edit or myRequest.edit2,
                            "create" : myRequest.create,
                            "delete" : False,
                            "download" : True
                        }))
                        
                        action = "Editar" if myRequest.edit else "Crear"
                        
                        self.registerLog(action, idFile)
                    
                    newNotifY.description = f"Se ha aprovó tu solicitud referente al archivo {myRequest.nameFile}"
                    newNotifY.permission = newPermission.id
                    self.session.add_all([newNotifY, newPermission])
                    
                    data = {
                        "subject" : "Archivo compartido desde AI-rchive",
                        "recipients" : myRequest.emails.split(", "),
                        "body" : f"{userRe.names} ha querido compartir este archivo contigo"
                    }
                    
                    
                if(myRequest.delete):
                    delete = self.session.query(File).filter(File.secureName == self.createSecureName(myRequest.nameFile), File.dependenceId == myRequest.dependenceId, File.clasificationId == myRequest.clasificationId).first()
                    os.remove(f"{getWorkSpace()}{delete.route}")
                    try:
                        os.remove(f"{getWorkSpace()}{myRequest.routeFileRequest}")
                    except:
                        pass
                    delete.view = False
                    self.session.add(delete)
                    
                    data = {
                        "subject" : "Archivo eliminado AI-rchive",
                        "recipients" : [userRe.email],
                        "body" : f"Se ha eliminado de forma correcta el archivo que solicitaste"
                    }
                    
                    self.registerLog("Eliminar", delete.id)
                    
                
            else:
                newNotifY.description = f"Se ha rechazó tu solicitud referente al archivo {myRequest.nameFile}. detalles: {json.details}"
                self.session.delete(myRequest)
                os.remove(f"{getWorkSpace()}{myRequest.routeFileRequest}")
                data = {
                    "subject" : "Solicitud rechazada AI-rchive",
                    "recipients" : [userRe.email],
                    "body" : f"Se ha rechazado tu sólicitud. A continuación los motivos: {json.details}"
                }
                
            notfy = self.session.query(Notification).filter(Notification.requestId == myRequest.id).first()
            self.session.delete(notfy)
                
            self.session.commit()
            self.mail.sendMail(data=data,archive=file
            )
            
            
            
            return "Respuesta enviada"
                
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            self.session.rollback()
            raise Exception("Algo salió mal")
        
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
            print(e)
            raise Exception("Al parecer este archivo ya no existe, refresque la página.")
    
    #Gets
    
    def getFiles(self):
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
                    if archive.view:
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
                files = self.session.query(File).filter(File.view == True).all()
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
            print(e)
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
        
    def registerLog(self, action:str, fileId:UUID):
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
        
    def getDocument(self, id:UUID, download=False):
        self.registerLog("Descarga" if download else "Ver", id)
        file = self.session.get(File, id)
        return send_file(path_or_file=f"{getWorkSpace()}{file.route}", as_attachment=download)
    
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
                "create" : dependence.acronym == "CIN",
                "chatIA" : user.admin or dependence.acronym != "CIN"
            }
            
            if dependence.acronym != "CIN":
                for permission in user.permissions:
                    if permission.create:
                        response["create"] = True
            return response
        except Exception as e:
            print(e)
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
            print(e)
            raise Exception("Algo ha pasado")
        
    def getDetailsRequest(self, id:UUID):
        try:
            request = self.session.get(Request, id)
            
            print(request.getDict())
            
            permission = None
            
            if request.edit2:
                permission = "Reclasificación / cambio de código"
            elif request.edit:
                permission = "Modificación"
            elif request.delete:
                permission = "Eliminación"
            elif request.create:
                permission = "Creación"
            elif request.download:
                permission = "Descargar"
            
            return {
                "description" : request.description,
                "permission" : permission,
                "name" : request.nameFile,
                "emails" : request.emails
            }
        except Exception as e:
            print(e)
            Exception("Algo ha pasado")
            
            
    def getLogs(self):
        try:
            logs = self.session.query(Log).all()
            
            response = []
            
            for log in logs:
                
                archive = self.session.get(File, log.fileId)
                user = self.session.get(User, log.userId)
                name = archive.route.split("/")[-1]
                response.append({
                    "extension" : archive.extension,
                    "name" :  f"{name} - Usuario: {user.names}",
                    "date" : self.getDateString(log.createAt),
                    "action" : log.action
                })
            return response
        except Exception as e:
            print(e)
            raise Exception("No se pudo obtener el Log")