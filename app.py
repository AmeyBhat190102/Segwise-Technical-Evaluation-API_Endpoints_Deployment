from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
auth = HTTPBasicAuth()

# Create a simple user authentication dictionary
users = {
    "admin": "password123"
}


@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
