import os
from flask import Flask
from flask_restx import Api
from db import db
from resources.course import Course, Courses, Roadmap
from resources.vote import Vote

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///course-api.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = os.environ.get("app_secret_key", "daskldsaf#@%$#@$cc")

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Course,"/course")
api.add_resource(Courses,"/courses")
api.add_resource(Vote,"/vote")
api.add_resource(Roadmap, "/roadmap/<string:courses_ids>")

if __name__ == "__main__":
    db.init_app(app)
    app.run()