from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    date = db.Column(db.String)

    def json(self):
        return {'id': self.id, 'question': self.question, 'answer': self.answer, 'date': self.date}


with app.app_context():
    db.create_all()


@app.route('/questions', methods=['POST'])
def obtain_questions():
    number_request = request.json
    questions_number = number_request['questions_num']
    questions = requests.get("https://jservice.io/api/random?count=" + str(questions_number))
    try:
        previous_question = Question.query.all().pop()
    except:
        previous_question = None

    for i in range(0, questions_number):
        new_question = Question(id=questions.json()[i]['id'],
                                question=questions.json()[i]['question'],
                                answer=questions.json()[i]['answer'],
                                date=questions.json()[i]['created_at'])
        db.session.add(new_question)
        db.session.commit()

    try:
        return make_response(previous_question.json(), 200)
    except:
        return None

