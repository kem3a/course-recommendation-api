from db import db
from datetime import datetime

class CourseModel(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String(120), nullable = False)
    provider = db.Column(db.String(60), nullable = False)
    career = db.Column(db.String(60), nullable = False)
    level = db.Column(db.String(6), nullable = False)
    access_type = db.Column(db.String(4), nullable = False)
    votes = db.Column(db.Integer, default = 0, nullable = False)
    last_updated_utc = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)
    created_by = db.Column(db.String(15), nullable = False)
    def __init__(self, title, provider, career, level, access_type, created_by):
        self.title = title
        self.provider = provider
        self.career = career
        self.level = level
        self.access_type = access_type
        self.created_by = created_by
        
    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "provider": self.provider,
            "career": self.career,
            "level": self.level,
            "access_type" : self.access_type,
            "votes": self.votes,
            "last_updated_utc" : str(self.last_updated_utc)
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod    
    def find_course(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()
    
    @classmethod
    def find_courses(cls, **kwargs):        
        limit = kwargs.pop("limit")
        if "q" in kwargs:
            q= kwargs.pop("q")
            return cls.query.filter_by(**kwargs).filter(cls.title.contains(q)).order_by(cls.votes.desc()).limit(limit).all()
        return cls.query.filter_by(**kwargs).order_by(cls.votes.desc()).limit(limit).all()