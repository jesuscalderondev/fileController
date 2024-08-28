from app.domain.controller import appServices
from abstracts.objects import Json
from abstracts.controller import FunctionControler
from flask import request
from uuid import UUID

class Application():
    
    service = appServices()
    
    def login(self, request):
        data = Json(request.get_json())
        return FunctionControler.operate(self.service.login, [data.email, data.password], "token")
    
    def getFiles(self, state:int):
        view = state == 1 
        return FunctionControler.operate(self.service.getFiles, [view],key="files")
    

    def getClasifications(self):
        return FunctionControler.operate(self.service.getClasifications, key="clasifications")
    
    def getDependencies(self):
        return FunctionControler.operate(self.service.getDepencencies, key="dependencies")
    
    def registerFile(self, request):
        data = request.form.to_dict()
        json = Json(data)
        print(json.buildClass())
        archive = request.files["file"]
        
        return FunctionControler.operate(self.service.registerFile, [json, archive])
    
    def getDocument(self, id:str, down:int):
        return self.service.getDocument(UUID(id), down)
    
    def getPermissions(self):
        return FunctionControler.operate(self.service.getPermissions, key="permissions")
    
    def questionAi(self, request):
        question = request.get_json()["question"]
        return FunctionControler.operate(self.service.questionAi, [question], key="answer")
    
    def registerRequest(self, request):
        json = Json(request.form.to_dict())
        file = request.files["file"]
        print(file.filename)


        return FunctionControler.operate(self.service.registerRequest, [json, file])
    
    def getNotifications(self):
        return FunctionControler.operate(self.service.getNotifications, key="notifications")
    
    def getDetailsRequest(self, id:str):
        return FunctionControler.operate(self.service.getDetailsRequest, [UUID(id)], "request")
    
    def responseRequest(self, request):
        file = request.files["file"]
        json = Json(request.form.to_dict())
        return FunctionControler.operate(self.service.responseRequest, [json, file])
    
    def deleteFile(self, id):
        return FunctionControler.operate(self.service.deleteFile, [UUID(id)])
    
    def getLogs(self):
        return FunctionControler.operate(self.service.getLogs, key="logs")

    def getDocumentWithDirectory(self, directory:str, name:str):
        return self.service.getDocumentWithDirectory(directory, name)
    
    def backArchive(self, id):
        return FunctionControler.operate(self.service.backArchive, [UUID(id)])
    
    def downloadHistory(self):
        return self.service.downloadHistory()
    
    def shareArchive(self, request):
        return FunctionControler.operate(self.service.shareArchive, [Json(request.get_json())])