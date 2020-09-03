from app.models import db, User, Activity, Route
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
import datetime
import math


api = Namespace("activities", description="Create, Update and Delete activities")
latlng = api.model("LatLng", {
                            "lat": fields.Float(description="Path latitude"),
                            "lng": fields.Float(description="Path longitude")
                        })

coordinates = api.model('Route coordinates', {
                                'path': fields.List(fields.Nested(latlng))
                            })

model = api.model("Activity", {
                            "type": fields.String(required=True, description="Activity type.", example="Run"),
                            "title": fields.String(description="Name your workout.", example="Sunday Morning Wake up Run"),
                            "start_time": fields.Date(required=True,description="Specify start time of your workout.", example="2020-08-18 08:15:10"),
                            "end_time": fields.Date(required=True, description="Specify end time of your workout.", example="2020-08-18 09:10:05"),
                            "distance": fields.Integer(required=True, description="Specify the distance for the workout in meters.", example="5030"),
                            "effort_level": fields.Integer(description="Specify effort level for your workout from 0 to 10.", example="4"),
                            "route": fields.Nested(coordinates)
                            })

@api.route("/")
class UserActivities(Resource):
    @api.response(200, "No activities found for the specified user")
    @api.doc(security='token')
    @jwt_required
    def get(self):
        '''Get all activities for the user'''
        userId = get_jwt_identity()

        if userId == None:
            return {"message": "Not a valid user access token send "}, 404

        activities = Activity.query.filter(Activity.user_id==userId).all()
        data = [activity.to_dictionary() for activity in activities]
        return {"activities" : data}

    @api.expect(model)
    @jwt_required
    def post(self):
        '''Record activity for the user'''
        userId = get_jwt_identity()
        if userId == None:
            return {"message": "Not a valid user access token send "}, 404

        user = User.query.get(userId)
        if user == None:
            return {"message": "No user found for the requested id"}, 404

        data = api.payload
        route = data["route"]
        path = route["path"]
        routes= [Route(**latlng) for latlng in path]

        data.pop("route")
        activity = Activity(**data)
        activity.route = routes
        duration = get_duration(api.payload["start_time"], api.payload["end_time"])
        calories = get_calories(duration, user)
        pace = calc_pace(api.payload["distance"], duration)

        activity.calories = calories
        activity.user_id = userId
        activity.pace = pace
        db.session.add(activity)
        db.session.commit()
        return {"message": "Successfully recorded activity."}, 201



@api.route("/<int:id>")
class UserActivity(Resource):
    @api.response(200, "No activities found for the specified user")
    @api.doc(security='token')
    @jwt_required
    def get(self, id):
        '''Get activity by id for the user'''
        userId = get_jwt_identity()
        if userId == None:
            return {"message": "Not a valid user access token send "}, 404

        activity = Activity.query.get(int(id))
        return {"activity" : activity.to_dictionary()}


def get_duration(start_time, end_time):
    # 2020-08-18 08:15:10 format
    start = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    duration = ((end - start).total_seconds())/60
    return duration

def get_calories(duration, user):
    # calculate the calories burned for a male
    if user.gender == 1:
        return calc_calories(0.2017, 0.09036, 0.6039, 55.0969, duration, user)
    # calculate the calories burned for a female
    if user.gender == 2:
        return calc_calories(0.074, 0.05741, 0.4472, 20.4022, duration, user)

def calc_calories(age_rate, weight_rate, heart_rate, rate, duration, user):
    #TODO in the future get the actual heart rate, currently is hard coded to the avg heart rate
    calories_burned = ((user.age * age_rate) + (user.weight * weight_rate) + (100 * heart_rate) - rate) * ( duration / 4.184)
    return calories_burned

def calc_pace(distance, duration):
    # distance is stored in meters, so we have to convert it KM to calculate pace correctly
    kilometers = int(distance) / 1000
    return math.ceil(duration / kilometers)
