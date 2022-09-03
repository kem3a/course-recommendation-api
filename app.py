import os
from flask import Flask
from flask_restx import Api
from db import db
from resources.course import Course, Roadmap, ns as ns1
from resources.vote import Vote, ns as ns2
from resources.report import Report,ns as ns3

app =Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///course-api.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = os.environ.get("APP_SECRET_KEY", "daskldsaf#@%$#@$cc")

db.init_app(app)

api = Api(app, version='1.0', title='Course Recommendation API',
    description='''Course Recommendation API is a simple API that allows learners to recommend courses and get recommended courses
    -
    https://github.com/kem3a/course-recommendation-api''')

# TODO (Abdulkareem):
#  best practice:
#  1- format files before every commit
#  2- all configs in a config file
#  3- all redundant (e.g. parsers, models, expected ... etc) should be in a separate file.
#  4- use methods in utils file.
# TODO (NOT DONE)
@app.before_first_request
def create_tables():
    db.create_all()

api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)

ns = api.namespace("courses", "Courses operations")

ns.add_resource(Course,"/")
ns.add_resource(Vote,"/votes/<int:course_id>")
ns.add_resource(Roadmap, "/roadmaps/<string:courses_ids>")
ns.add_resource(Report, "/report/<string:course_id>")


if __name__ == "__main__":
    app.run()