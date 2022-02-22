from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
marsh = Marshmallow()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String,unique=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    bio = db.Column(db.String,nullable=True)
    hobby = db.Column(db.String,nullable=True)
    address = db.Column(db.String,nullable=True)
    image = db.Column(db.Text,nullable=True)

    def __init__(self,username,password,email,image):
        self.username=username
        self.email=email
        self.password=password
        self.image=image

class UserSerializer(marsh.Schema):
    class Meta:
        fields = ['username','email','bio','hobby','address']

SingleUser = UserSerializer()
AllUsers = UserSerializer(many = True)
