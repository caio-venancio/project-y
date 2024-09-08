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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/uai-db'
# os.getenv('DATABASE_URL')

# Initialize Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes

print("terminando init")