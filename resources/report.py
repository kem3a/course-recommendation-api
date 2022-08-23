from flask_restx import Resource, reqparse
from models.report import ReportModel

class Report(Resource):

    def post(self, course_id):
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
