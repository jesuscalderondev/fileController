from flask import jsonify

class EndPoint:

    response = {"vacio" : "está vacio"}

    def __init__(self, func, data=None, error="Error Basic"):
        try:
            operate = func(data) if data != None else func()
            self.response =  jsonify(operate), 200
        except Exception as e:
            self.response = jsonify(message = f'{e}', error = error), 403

    