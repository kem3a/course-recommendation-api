from db import db

class VoteModel(db.Model):
    __tablename__ = "votes"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    created_by = db.Column(db.String(15))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    course = db.relationship("CourseModel")
    
    def __init__(self, course_id, created_by):
        self.course_id = course_id
        self.created_by = created_by

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod    
    def find_vote(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()