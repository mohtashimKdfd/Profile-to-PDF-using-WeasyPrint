from flask import Flask, Blueprint, request, jsonify, render_template, make_response
from flask_restx import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import User, SingleUser, AllUsers, db
from flask_weasyprint import HTML, render_pdf
from src.config.error_codes import error
from src.parsers.all_parsers import signup_parser, login_parser

app = Blueprint('app', __name__)
api = Api(app)

@api.route('/')
class Home(Resource):
    def get(self):
        return 'Flask is up and running'

@api.route('/signup')
class Signup(Resource):
    @api.expect(signup_parser)
    def post(self):
        args = signup_parser.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']
        hashed_password = generate_password_hash(password)
        image = args['image']

        if User.query.filter_by(username=username).count():
            return jsonify({'msg':'User already registered'})
        else:
            newUser = User(username=username, email=email, password=hashed_password,image=image)
            try:
                db.session.add(newUser)
                db.session.commit()
                return SingleUser.jsonify(newUser)
            except Exception as e:
                print(e)
                return {
                    'status':error['500'],
                    'msg':'Error in creating user'
                },500
    def get(self):
        return jsonify({'msg':'Method not allowed'})


@api.route('/login')
class Login(Resource):
    @api.expect(login_parser)
    def post(self):
        args = login_parser.parse_args()
        email = args['email']
        password = args['password']
        if User.query.filter_by(email=email).count():
            targetUser = User.query.filter_by(email=email).first()
            if check_password_hash(targetUser.password,password)==True:
                html = render_template('profile.html',user=targetUser)
                # return html   
                return render_pdf(HTML(string=html))
            else:
                return jsonify({'msg':'Wrong password'})
        else:
            return jsonify({'msg':'No user found'})
    def get(self):
        return make_response(render_template('login.html'))


@api.route('/update/<id>')
class Update(Resource):
    def post(self,id):
        TargetUser = User.query.filter_by(id=id).first()
        if not TargetUser:
            return jsonify({'msg':'No user found'})
        else:
            bio = request.form['bio']
            address = request.form['address']
            hobby = request.form['hobby']
            TargetUser.bio = bio
            TargetUser.address = address
            TargetUser.hobby = hobby
            db.session.commit()
            html = render_template('profile.html',user=TargetUser)
            return render_pdf(HTML(string=html))
    def get(self,id):
        TargetUser = User.query.filter_by(id=id).first()
        if TargetUser:
            return make_response(render_template('update.html',user=TargetUser))
        else:
            return jsonify({'msg':'No user found'})