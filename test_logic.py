from app.domain.controller import appServices
from abstracts.objects import Json

app = appServices()

def testCreateUser():
    operation = False
    try:
        dictionary = {
            "names" : "Nombre De Prueba",
            "password" : app.passwordHash("pass"),
            "email" : "prueba@gmail.com",
            "admin" : True
        }

        json = Json(dictionary)

        app.registerNewUser(json)
        operation = True
    except Exception as e:
        print(e)

    assert operation

def testCreateDependence():

    try:
        dictionary = {
            "name" : "Control de calidad",
            "directory" : app.createSecureName("Control de calidad"),
            "acronym" : "CDC"
        }

        json = Json(dictionary)

        app.registerDependence(json)

        assert True
    except Exception as e:
        print(e)
        assert False
