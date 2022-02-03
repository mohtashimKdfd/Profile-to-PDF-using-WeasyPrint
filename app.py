from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://mohtashimkamran:kamran@127.0.0.1/test2.db'

db = SQLAlchemy(app)
marsh = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String,unique=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    bio = db.Column(db.String,nullable=True)
    hobby = db.Column(db.String,nullable=True)
    address = db.Column(db.String,nullable=True)

    def __init__(self,username,password,email):
        self.username=username
        self.email=email
        self.password=password

class UserSerializer(marsh.Schema):
    class Meta:
        fields = ['username','email','bio','hobby','address']

SingleUser = UserSerializer()
AllUsers = UserSerializer(many = True)


@app.route('/')
def index():
    return "Uell0"

@app.route('/signup',methods=['POST'])
def signup():
    if request.method=='POST':
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        hashed_password = generate_password_hash(password)

        if User.query.filter_by(username=username).count():
            return jsonify({'msg':'User already registered'})
        else:
            newUser = User(username=username, email=email, password=hashed_password)
            try:
                db.session.add(newUser)
                db.session.commit()
                return SingleUser.jsonify(newUser)
            except Exception as e:
                print(e)
                return jsonify({'msg':'Error in creating user'})

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).count():
            targetUser = User.query.filter_by(email=email).first()
            if check_password_hash(targetUser.password,password)==True:
                return render_template('profile.html',user=targetUser)
            else:
                return jsonify({'msg':'Wrong password'})
        else:
            return jsonify({'msg':'No user found'})
    else:
        return render_template('login.html')
if __name__ == '__main__':
    app.run(debug=True)