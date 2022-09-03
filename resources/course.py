from flask_restx import Resource, reqparse, Namespace, fields
from models.course import CourseModel

ns = Namespace("courses", "Courses operations")
course_model = ns.model("course_model", {
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
ns.add_model("course_model", course_model)


class Course(Resource):
    course_parser = reqparse.RequestParser(trim=True)
    course_parser.add_argument('title', type=str, required=True, case_sensitive=False,
                               help="This field cannot be left blank!")
    course_parser.add_argument('provider', type=str, required=True, case_sensitive=False,
                               help="This field cannot be left blank!")
    course_parser.add_argument('career', type=str, required=True, case_sensitive=False,
                               help="This field cannot be left blank!")
    course_parser.add_argument('level', type=str, required=True, case_sensitive=False,
                               choices=["entry", "mid", "senior"],
                               help="This field must contain one of these three values (entry, mid, senior)")
    course_parser.add_argument('access_type', type=str, required=True, case_sensitive=False, choices=["free", "paid"],
                               help="This field must contain one of these two values (free, paid)")

    search_parser = reqparse.RequestParser(trim=True)
    search_parser.add_argument('q', type=str, required=False, case_sensitive=False,
                               help="A word to look for in course titles", location="args")
    search_parser.add_argument('provider', type=str, required=False, case_sensitive=False, help="Course provider name",
                               location="args")
    search_parser.add_argument('career', type=str, required=False, case_sensitive=False,
                               help="The career the course is intended/recommended for", location="args")
    search_parser.add_argument('level', type=str, required=False, case_sensitive=False,
                               help="The career level the course is intended/recommended for",
                               choices=["entry", "mid", "senior"], location="args")
    search_parser.add_argument('access_type', type=str, required=False, case_sensitive=False, help="Type of access",
                               choices=["free", "paid"], location="args")
    search_parser.add_argument('limit', type=int, default=10, required=False, help="The number of records returned",
                               location="args")

    delete_parser = reqparse.RequestParser(trim=True)
    delete_parser.add_argument('id', type=int, required=True, help="This field cannot be left blank!", location="args")

    @ns.doc("get_courses")
    @ns.expect(search_parser)
    @ns.response(code=200, description="OK", model=fields.List(fields.Nested(course_model)), envelope='courses')
    def get(self):
        '''Returns a list of courses based on query parameters'''
        args = Course.search_parser.parse_args()
        data = {k: v for k, v in args.items() if v}
        return {"courses": [course.json() for course in CourseModel.find_courses(**data)]}, 200

    @ns.doc("add_course")
    @ns.expect(course_model)
    @ns.response(code=201, description="CREATED", model=course_model)
    def post(self):
        '''Add a course'''
        data = Course.course_parser.parse_args()
        course = CourseModel.find_course(**data)
        if course:
            return {"message": "A course with the same details already exists.",
                    "hint": "Use the /vote endpoint to vote.",
                    "course": course.json()}, 409

        course = CourseModel(**data, created_by=reqparse.request.remote_addr)
        try:
            course.save_to_db()
        except:
            return {"message": "An error occurred adding the course."}, 500
        return course.json(), 201

    @ns.doc("delete_course")
    @ns.expect(delete_parser)
    @ns.response(code=200, description="OK", model=fields.Raw(example={"message": "Course deleted"}))
    def delete(self):
        '''Delete a course'''
        data = Course.delete_parser.parse_args()
        course = CourseModel.find_course(**data)
        if course:
            if not course.created_by == reqparse.request.remote_addr:
                return {'message': 'You did not add the course or your ip address has changed.'}, 401
            try:
                course.delete_from_db()
            except:
                return {"message": "An error occurred deleting the course."}, 500
            return {'message': 'Course deleted.'}, 200

        return {'message': 'Course not found.'}, 404


class Roadmap(Resource):

    @ns.doc("get_roadmap")
    @ns.doc(params={"courses_ids": "List of course IDs separated by a hyphen"})
    @ns.response(code=200, description="OK", model=fields.List(fields.Nested(course_model)), envelope='courses')
    def get(self, courses_ids):
        '''Returns a list of courses based on given course IDs '''
        courses_ids_list = courses_ids.split("-")
        courses = []
        for i in range(len(courses_ids_list)):
            try:
                courses_ids_list[i] = int(courses_ids_list[i])
                courses.append(CourseModel.find_course(id=courses_ids_list[i]).json())
            except:
                return {"message": "Roadmap should contain a list of valid course ids separated by a hyphen.",
                        "example": "{}roadmaps/1-2-3-4-5".format(reqparse.request.root_url)}, 400

        return {"courses": courses}, 200