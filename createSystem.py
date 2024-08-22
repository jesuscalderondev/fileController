from app.domain.controller import appServices
from app.domain.models import *
from abstracts.objects import Json

app = appServices()
session = model.Session


#Register all dependencies

dependencies = {
    "GER" : "Gerencia",
    "ADF" : "Administración y Financiera",
    "GHU" : "Gestión Humana",
    "TEC" :"Técnica",
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
            "directory" : app.createSecureName(dependencies[dependence])
        }
    )
    
    app.registerDependence(json)

# Register all clasifications
clasifications = {
    "P" : "Procedimiento",
    "I" : "Instructivo",
    "M" : "Manual",
    "C" : "Código",
    "D" : "Política, reglamento, plan, programa, protocolo, caracterizaciones",
    "PR" : "Programa",
    "R" : "Registro (Formato)"
}

for clasification in clasifications.keys():
    json = Json(
        {
            "name" : clasifications[clasification],
            "acronym" : clasification,
        }
    )
    
    app.registerClasification(json)

#Register all user

users = [
    {
        "names" : "Administrador Control Interno",
        "admin" : True,
        "email" : "admin@conint.com",
        "password" : app.passwordHash("pass"),
        "dependenceId" : session.query(Dependence).filter(Dependence.acronym == "CIN").first().id
    },
    
    {
        "names" : "Administrador Gerencia",
        "admin" : False,
        "email" : "admin@ger.com",
        "password" : app.passwordHash("pass"),
        "dependenceId" : session.query(Dependence).filter(Dependence.acronym == "GER").first().id
    }
]

for user in users:
    
    print(user)
    
    json = Json(user)
    app.registerUser(json)
    
#Register all Files

files = [
    {
        "extension" : "xlsx",
        "name" : "Plantillas de pago",
        "secureName" : app.createSecureName("Plantillas de pago"),
        "dependenceId" : session.query(Dependence).filter(Dependence.acronym == "GER").first().id,
        "clasificationId" : session.query(Clasification).filter(Clasification.acronym == "P").first().id
    }
]

for fileA in files:
    
    json = Json(fileA)
    
    app.registerFile(json)