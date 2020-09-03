from app.models import db, User
from flask_jwt_extended import create_access_token
from flask_restx import Resource, Namespace, fields


api = Namespace('auth', description='User authorization related operations')

login_model = api.model("Login", {
                            "email": fields.String(required=True, description="Unique email address.", example="demo@user.com"),
                            "password": fields.String(required=True, description="User Password.", example="password"),
                            })

signup_model = api.clone("Signup", login_model, {
                            "name": fields.String(required=True, description="User first name.", example="Joana"),
                            "lastname": fields.String(required=True, description="User lastname.", example="Kamp"),
                            })


@api.route("/signup")
class Signup(Resource):
    @api.expect(signup_model)
    # TODO add expected return errors
    def post(self):
        '''Create a user record on a signup'''
        user = User.query.filter_by(email=api.payload["email"]).first()
        if user:
            return {"message": "This email is already registered"} , 409
        else:
            user = User(**api.payload)
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(identity=user.id)
            return {
                    "token": access_token,
                    "message" : " Successfull registered user" }, 201

@api.route("/login")
class Login(Resource):
    # TODO add expected return errors
    @api.expect(login_model)
    def post(self):
        '''Get user info and access token for a login request'''
        user = User.query.filter_by(email=api.payload["email"]).first()

        if user:
            valid = user.check_password(api.payload["password"])

            if valid:
                access_token = create_access_token(identity=user.id)
                return {
                    "token":access_token,
                    "name":user.name,
                    "lastname":user.lastname,
                    "gender":user.gender,
                    "weight":user.weight,
                    "age":user.age
                }
            else:
                return { "message":  "Incorrect email or password."} , 401

        else:
            return { "message":  "Incorrect email or password."} , 401
