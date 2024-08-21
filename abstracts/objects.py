class Json():

    dictionary = None

    def __init__(self, dictionary:dict):
        self.dictionary = dictionary
        for atribute in dictionary:
            setattr(self, atribute, dictionary[atribute])
    
    def getNewDictionary(self, parameters:list=[]):
        newDict = {}
        if parameters != []:
        
            for parameter in parameters:
                param = getattr(self, parameter)
                newDict[parameter] = param
        else:
            newDict = self.buildClass()
                
        return newDict

    def buildClass(self):
        return self.__dict__
    
    def add(self, name:str, value:any):
        setattr(self, name, value)

    