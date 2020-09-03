from dotenv import load_dotenv
from paths import path1, path2, path3, path4, path5

load_dotenv()

from app import app, db
from app.models import (User, Activity, Route)

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(
        name="Joana",
        lastname="Smith",
        hashed_password="pbkdf2:sha256:150000$nNvIYhGF$8f07bb456ecdcad6ed1bdd02a2c200a6f315af6c7cbce267c9add238cbf78e89",
        email="demo@user.com",
        gender=2,
        weight=64.3,
        age=33
    )

    activity1 = Activity(
        type= "Run",
        title= "Langus Riverfront trail",
        start_time = "2020-08-20 08:15:10",
        end_time = "2020-08-20 09:30:05",
        distance = "7530",
        effort_level = "3",
        calories = 300,
        pace = 11,
    )

    routes = []
    for path in path1:
        route = Route (
            lat = path["lat"],
            lng = path["lng"],
            timestamp = "2020-08-18"
        )
        routes.append(route)

    activity1.route = routes
    activity1.user = user

    activity2 = Activity(
        type= "Run",
        title= "Morning Run",
        start_time = "2020-08-21 05:15:10",
        end_time = "2020-08-21 07:30:05",
        distance = "6530",
        effort_level = "5",
        calories = 400,
        pace = 10,
    )


    routes2 = []
    for path in path2:
        route2 = Route (
            lat = path["lat"],
            lng = path["lng"],
            timestamp = "2020-08-18"
        )
        routes2.append(route2)

    activity2.route = routes2
    activity2.user = user

    activity3 = Activity(
        type= "Run",
        title= "Stress Free Run",
        start_time = "2020-08-22 09:15:10",
        end_time = "2020-08-22 10:10:05",
        distance = "4530",
        effort_level = "4",
        calories = 375,
        pace = 9,
    )


    routes3 = []
    for path in path3:
        route3 = Route (
            lat = path["lat"],
            lng = path["lng"],
            timestamp = "2020-08-18"
        )
        routes3.append(route3)

    activity3.route = routes3
    activity3.user = user

    activity4 = Activity(
        type= "Run",
        title= "Stress Free Run",
        start_time = "2020-08-23 09:15:10",
        end_time = "2020-08-23 10:10:05",
        distance = "4530",
        effort_level = "6",
        calories = 375,
        pace = 14,
    )


    routes4 = []
    for path in path4:
        route4 = Route (
            lat = path["lat"],
            lng = path["lng"],
            timestamp = "2020-08-18"
        )
        routes4.append(route4)

    activity4.route = routes4
    activity4.user = user

    activity5 = Activity(
        type= "Run",
        title= "Traning Run",
        start_time = "2020-08-24 09:15:10",
        end_time = "2020-08-24 10:10:05",
        distance = "7500",
        effort_level = "5",
        calories = 575,
        pace = 10,
    )


    routes5 = []
    for path in path5:
        route5 = Route (
            lat = path["lat"],
            lng = path["lng"],
            timestamp = "2020-08-18"
        )
        routes5.append(route5)

    activity5.route = routes5
    activity5.user = user

    activity6 = Activity(
        type= "Run",
        title= "Lunch Run",
        start_time = "2020-08-26 11:15:10",
        end_time = "2020-08-26 12:10:05",
        distance = "6530",
        effort_level = "3",
        calories = 480,
        pace = 11,
    )

    activity6.route = routes
    activity6.user = user


    db.session.add(activity1)
    db.session.add(activity2)
    db.session.add(activity3)
    db.session.add(activity4)
    db.session.add(activity5)
    db.session.add(activity6)


    db.session.commit()
