from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from os import environ
from Question import Question

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = environ.get('DB_URL')
db = SQLAlchemy(app)


@app.route('/questions', methods=['POST'])
def obtain_questions():
    try:
        questions_number = request.json
        questions = requests.get("https://jservice.io/api/random?count=" + str(questions_number['questions_num']))
        for i in range(0, questions_number['questions_num']):
            print(questions.json()[i]['id'])
            try:
                check = Question.query.filter_by(id=questions.json()[i]['id'])
                return make_response(jsonify({'message': 'question already obtained'}), 400)
            except Exception as e:
                new_question = Question(id=questions.json()[i]['id'],
                                        question=questions.json()[i]['question'],
                                        answer=questions.json()[i]['answer'],
                                        data=questions.json()[i]['data'])
                db.session.add(new_question)
                db.session.commit()
                return make_response(jsonify({'message': 'success'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error'}), 400)


if __name__ == "__main__":
    app.run()
