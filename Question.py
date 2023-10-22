from main import db


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    date = db.Column(db.Integer)
