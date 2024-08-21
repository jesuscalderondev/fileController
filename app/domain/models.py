from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, VARCHAR, Double, TIMESTAMP, Uuid, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from uuid import uuid4, UUID
import os
from datetime import datetime
from abstracts.controller import Service
from abstracts.objects import Json

from abstracts.database import Model, Table
model = Model("database", False)

class User(model.Base, Table):

    __tablename__ = "Users"

    names = Column(VARCHAR(3000), nullable=False)
    email = Column(VARCHAR(300), nullable=False, unique=True)
    password = Column(VARCHAR(3000), nullable=False)
    dependece = Column(Uuid, ForeignKey("Dependencies.id"))
    permissions = relationship("Permission", backref="user")
    admin = Column(Boolean, nullable=False, default=False)

    def __init__(self, json:Json):
        Model.createObject(self, json.buildClass())


class File(model.Base, Table):

    __tablename__ = "Files"

    num = Column(Integer, unique=True, autoincrement=True)
    extension = Column(VARCHAR(5), nullable=False)
    name = Column(VARCHAR(300), nullable=False)
    secureName = Column(VARCHAR(350), nullable=False)
    route = Column(VARCHAR(3000), nullable=False, unique=True)
    allowedUsers = relationship("Permission", backref="file")
    dependenceId = Column(Uuid, ForeignKey("Dependencies.id"), nullable=False)
    clasificationId = Column(Uuid, ForeignKey("Clasifications.id"), nullable=False)

    def __init__(self, json:Json):
        Model.createObject(self, json.buildClass())


class Permission(model.Base, Table):

    __tablename__ = "Permissions"

    userId = Column(Uuid, ForeignKey("Users.id"), nullable=False)
    fileId = Column(Uuid, ForeignKey("Files.id"), nullable=False)
    edit = Column(Boolean, nullable=False)
    delete = Column(Boolean, nullable=False)

    def __init__(self, json:Json):
        Model.createObject(self, json.buildClass())

class Dependence(model.Base, Table):

    __tablename__ = "Dependencies"

    name = Column(VARCHAR(300), nullable=False, unique=True)
    acronym = Column(VARCHAR(5), nullable=False, unique=True)
    files = relationship("File", backref="dependence")
    users = relationship("User", backref="dependence")
    directory = Column(VARCHAR(300), nullable=False)

    def __init__(self, json:Json):
        Model.createObject(self, json.buildClass())


class Clasification(model.Base, Table):

    __tablename__ = "Clasifications"

    acronym = Column(VARCHAR(5), nullable=False, unique=True)
    name = Column(VARCHAR(225), nullable=False)
    files = relationship("File", backref="clasification")