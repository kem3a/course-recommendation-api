from db import db

class ReportModel(db.Model):
    __tablename__ = "reports"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    created_by = db.Column(db.String(15), nullable = False)
    
    def __init__(self, course_id, created_by):
        self.course_id = course_id
        self.created_by = created_by

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod    
    def find_report(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()