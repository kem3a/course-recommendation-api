from flask_restx import Namespace, fields

courses_namespace = Namespace("courses", "Courses operations")
course_model = courses_namespace.model("course_model", {
    "id": fields.Integer(readonly=True, description="Course identifier", example=1),
    "title": fields.String(required=True, description="Course title", example="introduction to airflow in python"),
    "provider": fields.String(required=True, description="Course provider", example="datacamp"),
    "career": fields.String(required=True, description="The career the course is intended/recommended for",
                            example="data engineer"),
    "level": fields.String(required=True, description="The career level the course is intended/recommended for",
                           enum=["entry", "mid", "senior"], example="entry"),
    "access_type": fields.String(required=True, description="Type of access", enum=["free", "paid"], example="paid"),
    "votes": fields.Integer(readonly=True, description="Number of votes", example=27),
    "last_updated_utc": fields.String(readonly=True, description="Last modified", example="2022-08-24 18:15:18.270185")
})
courses_namespace.add_model("course_model", course_model)
