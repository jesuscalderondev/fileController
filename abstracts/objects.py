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
            newDict = self.dictionary
                
        return newDict
    
    def add(self, name:str, value:any):
        self.dictionary[name] = value