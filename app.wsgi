import sys
sys.path.insert(0, '/var/www/html/flask_project')
import os

os.environ["SECRET_KEY"] = "mysecretkey"
os.environ["WORKSPACE"] = "/var/www/html/flask_project/"

from server import app as application