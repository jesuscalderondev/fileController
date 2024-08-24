from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode
from datetime import datetime, timedelta
from uuid import UUID
import os
from flask import jsonify, request, render_template
from flask import session as cookies
from dotenv import load_dotenv
from extensions import mailer
import google.generativeai as genai
import os






load_dotenv()

class Service():
    
    mail = mailer
    
    genai.configure(api_key=os.environ.get("KEY_GEM"))
    model = genai.GenerativeModel(model_name="gemini-pro")
    
    def questionAi(self, question:str):
        try:
            response = self.model.generate_content([question]).text
            print(response)
            return response
        except Exception as e:
            print(e)
            raise Exception("No se puedo conectar")
        
    
    def passwordHash(self, password:str):
        return generate_password_hash(password)

    def passwordVerify(self, passHash:str, passUnHashed:str):
        return check_password_hash(passHash, passUnHashed)
    
    def getUser(self, request=None):
        try:
            if request is not None:
                token = request.headers.get('Authorization').split(" ")[1]
            else:
                token = cookies["token"]
            payload = decode(token, os.environ.get("SECRET_KEY"), algorithms=['HS256'])
            return UUID(payload.get('id'))
        except:
            return None
    
    def jwtRequired(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            
            if "session" in request.cookies:
                token = cookies["token"]

                if not token:
                    return jsonify({'error': 'Falta el token'}), 401

                try:
                    payload = decode(token, os.environ.get("SECRET_KEY"), algorithms=['HS256'])
                    print(self.getUser(request))
                except (ExpiredSignatureError, InvalidTokenError) as e:
                    if isinstance(e, ExpiredSignatureError):
                        return jsonify(error = 'T001', message = 'El token que ha proporcionado se encuentra vencido'), 401
                    elif isinstance(e, InvalidTokenError):
                        return jsonify(error = 'T000', message = 'El token que ha enviado no es válido'), 401
                return f(*args, **kwargs)
            else:
                return jsonify(error = 'T002', message = 'Falta el token de verificación, por favor incia sesión para obtener acceso'), 401

        return decorated
    
    def sessionRequired(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):

            if 'token' in cookies:
                token = cookies["token"]

                if not token:
                    return render_template("withOutSession.html")

                try:
                    payload = decode(token, os.environ.get("SECRET_KEY"), algorithms=['HS256'])
                    print(payload, "Este es el payload")
                except (ExpiredSignatureError, InvalidTokenError) as e:
                    if isinstance(e, ExpiredSignatureError):
                        return render_template("expiredSession.html")
                    elif isinstance(e, InvalidTokenError):
                        return render_template("invalidSession.html")
                return f(*args, **kwargs)
            return render_template("withOutSession.html")

        return decorated
    
    def creatreJWT(self, id):
        payload = {
            'id': str(id).replace("-", "")
        }
        token = encode(payload, os.environ.get("SECRET_KEY"), algorithm='HS256')

        return token
    
    def createSecureName(self, name):
        return secure_filename(name)
    
    def getNum(self, num:int) -> str:
        return "{:03d}".format(num)
    
    def getDateString(self, date:datetime):
        
        meses = ['enero', 'febrero', 'marzo', 'abril',
            'mayo', 'junio', 'julio', 'agosto',
            'septiembre', 'octubre', 'noviembre', 'diciembre'
        ]


        # Formato deseado: 25 de abril 2024 15:30
        formate = "%d de %B %Y %H:%M"
        month = meses[date.month - 1]
        
        minutes = "{:02d}".format(date.minute)
        
        dateFinish = f"{date.day} de {month} de {date.year} {date.hour}:{minutes}"

        return dateFinish
    
    
class FunctionControler:


    def operate(function, parameters = [], key:str = "message"):
        try:
            return {key : function(*parameters)}
        except Exception as e:
            raise Exception(e)
    