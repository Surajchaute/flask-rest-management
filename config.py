from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/pythondb'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY']  = "182KSK91023198jsds7878402940954*&*$@"
db = SQLAlchemy(app)


app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=3)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=5)
jwt = JWTManager(app)