from flask import Flask, jsonify, redirect, json, request, send_from_directory, render_template
from flask_cors import CORS
from abstracts.controller import Service
import os
from dotenv import load_dotenv
from uuid import uuid4, UUID
from abstracts.objects import Json
from extensions import mailer, getBackUp, getWorkSpace

load_dotenv()

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