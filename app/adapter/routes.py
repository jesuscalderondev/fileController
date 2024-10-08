from abstracts.microService import MicroService
from app.application.application import Application
from flask import request, render_template, session, redirect, url_for
from abstracts.route import EndPoint

routes = MicroService("routes").getBlueprint()
app = Application()

@routes.route('login', methods = ['POST'])
def login():
    return EndPoint(app.login, request).response

@routes.route('home', methods = ['GET'])
@app.service.sessionRequired
def home():
    return render_template('home.html')

@routes.route('requests', methods = ['GET'])
@app.service.sessionRequired
def requests():
    return render_template('sendRequests.html')

@routes.route('logOut', methods = ['GET'])
@app.service.sessionRequired
def logOut():
    session.pop("token")
    return redirect("/")

@routes.route('formFile', methods = ['GET'])
@app.service.adminRequired
def formFile():
    return render_template('formFile.html')

@routes.route('chatBot', methods = ['GET'])
@app.service.sessionRequired
def chatBot():
    return render_template('chatbot.html')

# Apis---------------------------------

@routes.route('getFiles/<int:state>', methods = ['GET'])
@app.service.jwtRequired
def getFiles(state):
    return EndPoint(app.getFiles, state).response



@routes.route('getClasifications', methods = ['GET'])
@app.service.jwtRequired
def getClasifications():
    return EndPoint(app.getClasifications).response

@routes.route('getDependencies', methods = ['GET'])
@app.service.jwtRequired
def getDependencies():
    return EndPoint(app.getDependencies).response

@routes.route('registerFile', methods = ['POST'])
@app.service.adminRequired
def registerFile():
    return EndPoint(app.registerFile, request).response

@routes.route('getDocument/<string:id>/<int:down>', methods = ['GET'])
@app.service.jwtRequired
def getDocument(id, down):
    return app.getDocument(id, down)

@routes.route('getDocumentUrl/<string:directory>/<string:name>', methods = ['GET'])
@app.service.jwtRequired
def getDocumentWithDirectory(directory, name):
    print(directory, name)
    return app.getDocumentWithDirectory(directory, name)

@routes.route('getPermissions', methods = ['GET'])
@app.service.jwtRequired
def getPermissions():
    return EndPoint(app.getPermissions).response

@routes.route('questionAi', methods = ['POST'])
@app.service.jwtRequired
def questionAi():
    return EndPoint(app.questionAi, request).response

@routes.route('registerRequest', methods = ['POST'])
@app.service.jwtRequired
def registerRequest():
    return EndPoint(app.registerRequest, request).response

@routes.route('getNotifications', methods = ['GET'])
@app.service.jwtRequired
def getNotifications():
    return EndPoint(app.getNotifications).response

@routes.route('view/<string:id>', methods = ['GET'])
@app.service.adminRequired
def view(id):
    return render_template('view.html',  idRequest = id)

@routes.route('getDetailsRequest/<string:id>', methods = ['GET'])
@app.service.adminRequired
def getDetailsRequest(id):
    return EndPoint(app.getDetailsRequest, id).response

@routes.route('responseRequest', methods = ['POST'])
@app.service.adminRequired
def responseRequest():
    return EndPoint(app.responseRequest, request).response

@routes.route('deleteFile/<string:id>', methods = ['GET'])
@app.service.adminRequired
def deleteFile(id):
    return EndPoint(app.deleteFile, id).response

@routes.route('log', methods = ['GET'])
@app.service.adminRequired
def log():
    return render_template('log.html')

@routes.route('deleteds', methods = ['GET'])
@app.service.adminRequired
def deleteds():
    return render_template('deleteds.html')

@routes.route('getLogs', methods = ['GET'])
@app.service.jwtRequired
def getLogs():
    return EndPoint(app.getLogs).response

@routes.route('backArchive/<string:fileId>', methods = ['GET'])
@app.service.jwtRequired
def backArchive(fileId):
    return EndPoint(app.backArchive, fileId).response

@routes.route('downloadHistory', methods = ['GET'])
@app.service.adminRequired
def downloadHistory():
    return app.downloadHistory()

@routes.route('update/<string:fileId>', methods = ['PUT'])
@app.service.jwtRequired
def update(fileId):
    return EndPoint(app.update, [fileId, request]).response

@routes.route('edit/<string:id>', methods = ['GET'])
@app.service.adminRequired
def edit(id):
    return render_template('edit.html',  idFile = id)

@routes.route('share/<string:id>', methods = ['GET'])
@app.service.adminRequired
def share(id):
    return render_template('share.html',  idFile = id)

@routes.route('share', methods = ['POST'])
@app.service.jwtRequired
def shareArchive():
    return EndPoint(app.shareArchive, request).response