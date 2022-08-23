import os
from flask import Flask
from flask_restx import Api
from db import db
from resources.course import Course, CourseDelete, Roadmap
from resources.vote import Vote
from resources.report import Report

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///course-api.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = os.environ.get("app_secret_key", "daskldsaf#@%$#@$cc")

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Course,"/courses")
api.add_resource(CourseDelete,"/courses/<string:course_id>")
api.add_resource(Vote,"/votes/<int:course_id>")
api.add_resource(Roadmap, "/roadmaps/<string:courses_ids>")
api.add_resource(Report, "/report/<string:course_id>")


if __name__ == "__main__":
    db.init_app(app)
    app.run()