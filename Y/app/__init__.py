print("Começando init")
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate




#pegando o .env
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
UPLOAD_FOLDER = 'app/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes

print("terminando init")