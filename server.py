from flask import Flask, jsonify, redirect, json, request, send_from_directory, render_template
from flask_cors import CORS
from abstracts.controller import Service
import os
from dotenv import load_dotenv
from uuid import uuid4, UUID
from abstracts.objects import Json
from extensions import mailer, getBackUp, getWorkSpace

load_dotenv()


from app.domain.controller import appServices
from app.domain.models import *
from abstracts.objects import Json
production = False

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


app.config['MAIL_SERVER'] = os.environ["MAIL_SERVER"]
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']

CORS(app, origins=['*'], supports_credentials=True)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/noENtrar")
def noEntrar():
    try:
        service = appServices()
        session = model.Session


        #Register all dependencies

        dependencies = {
            "GER" : "Gerencia",
            "ADF" : "Administración y Financiera",
            "GHU" : "Gestión Humana",
            "TEC" : "Técnica",
            "SST" : "Seguridad y Salud en el Trabajo",
            "JUR" : "Jurídica",
            "INF" : "Sistemas",
            "VEN" : "Ventas",
            "GDO" : "Gestión Documental",
            "CIN" : "Control Interno",
            "GRI" : "Gestión de Riesgos",
            "DES" : "Despliegue FTTH",
            "CON" : "Construcción FTTH",
            "CUM" : "Cumplimiento",
            "PAR" : "Parque Automotor"
        }

        for dependence in dependencies.keys():
            json = Json(
                {
                    "name" : dependencies[dependence],
                    "acronym" : dependence,
                    "directory" : service.createSecureName(dependencies[dependence])
                }
            )

            service.registerDependence(json)

        # Register all clasifications
        clasifications = {
            "P" : "Procedimiento",
            "I" : "Instructivo",
            "M" : "Manual",
            "C" : "Código",
            "D" : "Política, reglamento, plan, programa, protocolo, caracterizaciones",
            "R" : "Registro (Formato)"
        }

        for clasification in clasifications.keys():
            json = Json(
                {
                    "name" : clasifications[clasification],
                    "acronym" : clasification,
                }
            )

            service.registerClasification(json)

        #Register all user

        users = [
            {
                "names" : "Administrador Control Interno",
                "admin" : True,
                "email" : "admin@conint.com",
                "password" : service.passwordHash("pass"),
                "position" : "Auxiliar",
                "dependenceId" : session.query(Dependence).filter(Dependence.acronym == "CIN").first().id
            },

            {
                "names" : "Administrador Gerencia",
                "admin" : True,
                "email" : "jesusmcalderonv2002@gmail.com",
                "password" : service.passwordHash("pass"),
                "position" : "Distribuidor",
                "dependenceId" : session.query(Dependence).filter(Dependence.acronym == "GER").first().id
            },

            {
                "names" : "Auxiliar de gerencia",
                "admin" : False,
                "email" : "aux@ger.com",
                "password" : service.passwordHash("pass"),
                "position" : "Auxiliar",
                "dependenceId" : session.query(Dependence).filter(Dependence.acronym == "GER").first().id
            }
        ]

        for user in users:

            print(user)

            json = Json(user)
            service.registerUser(json)

        return "SIIIU"
    except Exception as e:
        return e

@app.route("/test")
def test():
    return render_template("testanimate.html")

from app.domain.models import model
model.createBase()

if not os.path.exists(getWorkSpace()):
    os.mkdir(getWorkSpace())
    
if not os.path.exists(getBackUp()):
    os.mkdir(getBackUp())
    
if not os.path.exists(f"{getWorkSpace()}requests"):
    os.mkdir(f"{getWorkSpace()}requests")
    
from app.adapter.routes import routes
app.register_blueprint(routes)

if __name__ == "__main__":
    mailer.mail.init_app(app)
    app.run(debug=True)