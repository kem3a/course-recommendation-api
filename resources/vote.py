from flask_restx import Resource, reqparse
from models.vote import VoteModel
from datetime import datetime

class Vote(Resource):   
    
    vote_parser = reqparse.RequestParser(trim=True)
    vote_parser.add_argument('course_id', type=int, required=True, help="This field cannot be left blank!")
    
    def post(self):
        data = Vote.vote_parser.parse_args()
        vote = VoteModel.find_vote(**data)
        if vote:
            return {"message":"A vote with the same details already exists."}, 409
        
        vote = VoteModel(**data, created_by=reqparse.request.remote_addr)
        try:
            vote.save_to_db()
            vote.course.votes = vote.course.votes + 1
            vote.course.last_updated_utc = datetime.utcnow()
            vote.save_to_db()
        except:
            return {"message": "An error occurred adding the vote."}, 500
        return {"message": "Vote successfully added."}, 201
        
    def delete(self):
        data = Vote.vote_parser.parse_args()
        vote = VoteModel.find_vote(**data, created_by=reqparse.request.remote_addr)
        if not vote:
            return {'message': 'You did not add a vote or your ip address has changed.'}, 404
        try:
            vote.course.votes = vote.course.votes - 1
            vote.course.last_updated_utc = datetime.utcnow()
            vote.delete_from_db()
        except:
            return {"message": "An error occurred deleting the vote."}, 500
        
        return {'message': 'vote deleted.'}, 200
    