from sqlalchemy import create_engine, inspect
from sqlalchemy import Column, Integer, VARCHAR, Double, TIMESTAMP, Uuid
from sqlalchemy.orm import sessionmaker, declarative_base
from uuid import uuid4, UUID
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class Model():

    Base = None
    Session = None

    def __init__(self, name, production = True):
        
        productionUrl = f'sqlite:///{os.environ.get("WORKSPACE")}{name}.sqlite'
        devUrl = f'sqlite:///{name}.sqlite'

        self.engine = create_engine(productionUrl if production else devUrl)
        Session = sessionmaker(self.engine)
        self.Session = Session()

        self.Base = declarative_base()

    def createBase(self):
        self.Base.metadata.create_all(self.engine)

    def createObject(obj, dictionary):
        obj.id = uuid4()
        obj.createAt = obj.updateAt = datetime.now()
        for atribute in dictionary:
            if atribute not in ["id", "createAt", "updateAt", "status"]:
                if "id" in atribute.lower():
                    try:
                        dictionary[atribute] = UUID(dictionary[atribute])
                    except:
                        print("Entra")
                        pass
                if "date" in atribute.lower():
                    try:
                        dictionary[atribute] = datetime.strptime(dictionary[atribute], "%Y-%m-%dT%H:%M")
                    except:
                        raise Exception(f"No pudo formatear {atribute}")
                setattr(obj, atribute, dictionary[atribute])

class Table(Model):

    id = Column(Uuid, primary_key=True, unique=True, nullable=False)
    createAt = Column(TIMESTAMP, nullable=False)
    updateAt = Column(TIMESTAMP, nullable=False)


    def getDict(self, skip = [], requiredList = []):

        data = {}
        private = ["password"]
        private.extend(skip)
        

        for atributte in self.__table__.columns:
            if atributte.name not in private:
                param = getattr(self, atributte.name)
                data[atributte.name] = param

        for required in requiredList:
            print(required)
            obj = getattr(self, required)
            if isinstance(obj, list):
                data[required] = [obj.getDict() for obj in obj]
            else:
                data[required] = True if ( obj != None and obj.expiredDate > datetime.now()) else False

        return data
    
    def update(self, dictionary:dict):

        keys = dictionary.keys()
        print(f"actualizando")

        for atributte in keys:
            if atributte not in ["id", "createAt", "updateAt"]:
                if "birthDate" == atributte:
                    dictionary["birthDate"] = datetime.strptime(dictionary["birthDate"], "%Y/%m/%d")
                elif "date" in atributte.lower():
                    print(f"es date {atributte}")
                    dictionary[atributte] = datetime.strptime(dictionary[atributte], "%Y-%m-%dT%H:%M")
                setattr(self, atributte, dictionary[atributte])
        self.updateAt = datetime.now()