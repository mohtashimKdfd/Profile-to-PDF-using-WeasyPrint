from flask_restx import reqparse

signup_parser = reqparse.RequestParser()

signup_parser.add_argument('username',type=str,required=True)
signup_parser.add_argument('password',type=str,required=True)
signup_parser.add_argument('image',type=str,required=True)
signup_parser.add_argument('email',type=str,required=True)


login_parser = reqparse.RequestParser()
login_parser.add_argument('email',type=str,required=True)
login_parser.add_argument('password',type=str,required=True)