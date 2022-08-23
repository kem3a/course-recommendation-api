from flask_restx import Resource, reqparse
from models.vote import VoteModel
from datetime import datetime

class Vote(Resource):   

    def post(self, course_id):
        data = {"course_id": course_id,
                "created_by": reqparse.request.remote_addr}
        vote = VoteModel.find_vote(**data)
        if vote:
            return {"message":"A vote with the same details already exists."}, 409
        
        vote = VoteModel(**data)
        try:
            vote.save_to_db()
            vote.course.votes = vote.course.votes + 1
            vote.course.last_updated_utc = datetime.utcnow()
            vote.save_to_db()
        except:
            return {"message": "An error occurred adding the vote."}, 500
        return {"message": "Vote successfully added."}, 201
        
    def delete(self, course_id):
        data = {"course_id": course_id,
                "created_by": reqparse.request.remote_addr}
        vote = VoteModel.find_vote(**data)
        if not vote:
            return {'message': 'You did not add a vote or your ip address has changed.'}, 404
        try:
            vote.course.votes = vote.course.votes - 1
            vote.course.last_updated_utc = datetime.utcnow()
            vote.delete_from_db()
        except:
            return {"message": "An error occurred deleting the vote."}, 500
        
        return {'message': 'vote deleted.'}, 200
    