from flask_restx import Resource, reqparse
from models.course import CourseModel


class Course(Resource):   
    
    course_parser = reqparse.RequestParser(trim=True)
    course_parser.add_argument('title', type=str, required=True, case_sensitive=False, help="This field cannot be left blank!")
    course_parser.add_argument('provider', type=str, required=True, case_sensitive=False, help="This field cannot be left blank!")
    course_parser.add_argument('career', type=str, required=True, case_sensitive=False, help="This field cannot be left blank!")
    course_parser.add_argument('level',type=str, required=True, case_sensitive=False, choices = ["entry","mid","senior"] , help="This field must contain one of these three values (entry, mid, senior)")
    course_parser.add_argument('access_type', type=str, required=True, case_sensitive=False, choices = ["free","paid"], help="This field must contain one of these two values (free, paid)")
    
    search_parser = reqparse.RequestParser(trim=True)
    search_parser.add_argument('q', type=str, required=False, case_sensitive=False, location = "args")
    search_parser.add_argument('provider', type=str, required=False, case_sensitive=False, location = "args")
    search_parser.add_argument('career', type=str, required=False, case_sensitive=False, location = "args")
    search_parser.add_argument('level',type=str, required=False, case_sensitive=False, location = "args")
    search_parser.add_argument('access_type', type=str, required=False, case_sensitive=False, location = "args")
    search_parser.add_argument('limit', type=int,default= 10 , required=False, location = "args")
    
    def get(self):
        args = Course.search_parser.parse_args()
        data = {k:v for k,v in args.items() if v}
        return {"courses":[course.json() for course in CourseModel.find_courses(**data)]}, 200
    
    def post(self):
        data = Course.course_parser.parse_args()
        course = CourseModel.find_course(**data)
        if course:
            return {"message":"A course with the same details already exists.", 
                    "hint": "Use the /vote endpoint to vote.",
                    "course":course.json()}, 409
        
        course = CourseModel(**data, created_by=reqparse.request.remote_addr)
        try:
            course.save_to_db()
        except:
            return {"message": "An error occurred adding the course."}, 500
        return course.json(), 201
      
      
class CourseDelete(Resource):
    
    def delete(self,course_id):
        course = CourseModel.find_course(id = course_id)
        print(reqparse.request.remote_addr)
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
    
    def get(self, courses_ids):
        courses_ids_list = courses_ids.split("-")
        courses = []
        for i in range(len(courses_ids_list)):
            try:
                courses_ids_list[i] = int(courses_ids_list[i])
                courses.append(CourseModel.find_course(id = courses_ids_list[i]).json())
            except:
                return {"message": "Roadmap should contain a list of valid course ids separated by a hyphen.",
                        "example": "{}roadmap/1-2-3-4-5".format(reqparse.request.root_url)}, 400
                
                
        return {"courses": courses}, 200