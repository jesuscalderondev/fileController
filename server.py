from flask import Flask, jsonify, redirect, json, request, send_from_directory, render_template
from flask_cors import CORS
from abstracts.controller import Service
import os
from dotenv import load_dotenv
from uuid import uuid4, UUID
from abstracts.objects import Json
import jwt

load_dotenv()

production = False

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

app.config['UPLOAD_FOLDER'] = (os.environ.get("WORKSPACE") if production else "") + "file/"

@app.route('/sources/<path:path>')
def send_image(path):
    print(path)
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)


""" app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SLS'] = False
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD'] """

CORS(app, origins=['*'], supports_credentials=True)

@app.route("/")
def index():
    return render_template('index.html')

from app.domain.models import model
model.createBase()

if not os.path.exists("files/"):
    os.mkdir("files")

if __name__ == "__main__":
    app.run(debug=True)