from app.models import db, User
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from flask_cors import CORS, cross_origin

api = Namespace('users', description='Create and update user operations')

model = api.model("User", {
                            "name": fields.String( description="User first name.", example="John"),
                            "lastname": fields.String( description="User last name.", example="Doe"),
                            "gender": fields.Integer( description="User's gender 1=Male; 2=Female; 0=Other.", enum=["1", "2"], example = "2"),
                            "weight": fields.Float( description="User's weight'.", example="64.5"),
                            "age": fields.Integer( description="User's integer.", example="34", min=14),
                            "image_url": fields.String( description="User Image URL.", example="/image.png"),
                          }
                )

@api.route("/<int:id>")
class GetUser(Resource):
    @api.response(200, 'User found')
    # TODO define error code for route
    def get(self, id):
        '''Get user by user id'''
        user = User.query.get(int(id))
        if user == None:
            return {"message": "No user found for the requested id"}, 404

        return {"user":user.to_dictionary()}

@api.route("/")
class UpdateUser(Resource):
    @api.doc('update_user')
    @api.response(201, 'User record updated')
    @api.expect(model)
    @jwt_required
    def put(self):
        '''Update user record using authorization token'''
        userId = get_jwt_identity()
        if userId == None:
            return {"message": "No user found for the requested id"}, 404

        db.session.query(User).filter(User.id==userId).update(api.payload)
        db.session.commit()

        return {"message":"User record updated successfully."}
