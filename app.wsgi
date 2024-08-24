import sys
sys.path.insert(0, '/var/www/html/flask_project')
import os

os.environ["BACKUP"]="backup/"
os.environ["WORKSPACE"]="files/"

os.environ["SECRET_KEY"]="BSDYABYDADA5DAVGASVGDSA45bhagyudas6"
os.environ["KEY_GEM"]="AIzaSyCTqW-QYDDUYalg11OykKJT8v8tajesfB4"
os.environ["MAIL_SERVER"]="smtp.gmail.com"
os.environ["MAIL_PORT"]=587
os.environ["MAIL_USERNAME"]="pabarros2003@gmail.com"
os.environ["MAIL_PASSWORD"]="l d v x k q i m g r r f a z n e"

from server import app as application