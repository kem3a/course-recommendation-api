from flask_restx import Resource, reqparse, Namespace, fields
from models.report import ReportModel

ns = Namespace("courses", "Courses operations")

class Report(Resource):
    
    @ns.doc("add_report")
    @ns.doc(params={"course_id":"Course identifier"})
    @ns.response(code=201,description="CREATED", model=fields.Raw(example={"message":"Report created."}))
    def post(self, course_id):
        '''Add a report'''
        data = {"course_id": course_id,
                "created_by": reqparse.request.remote_addr}
        
        report = ReportModel.find_report(**data)
        if report:
            return {"message":"A report with the same details already exists."}, 409
        
        report = ReportModel(**data)
        try:
            report.save_to_db()
        except:
            return {"message": "An error occurred adding the report."}, 500
        return {"message": "Report created."}, 201