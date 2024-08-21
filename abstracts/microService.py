from flask import Blueprint
import os


class MicroService():

    def __init__(self, blueprint:str):
        
        folderSource = os.path.abspath(os.getcwd())
        setattr(self, 'name', blueprint)

        self.bluePrint = Blueprint(self.name, self.name.upper(), f'{folderSource}/{blueprint}/static', url_prefix=f'/{blueprint}/')

    def getBlueprint(self) -> Blueprint:
        return self.bluePrint
