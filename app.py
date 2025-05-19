from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

# Init app and DB
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define question model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    clue = db.Column(db.Text, nullable=False) 
    response = db.Column(db.Text, nullable=False) 

    def to_dict(self):
        return {
            "category": self.category,
            "points": self.points,
            "clue": self.clue,
            "response": self.response
        }



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_question")
def get_question():
    category = request.args.get("category")
    points = int(request.args.get("points"))

    q = Question.query.filter_by(category=category, points=points).first()
    if q:
        return jsonify({
            "clue": q.clue,
            "response": q.response
        })
    else:
        return jsonify({
            "clue": "Clue not found.",
            "response": "No response available."
        })



@app.route("/answer", methods=["POST"])
def check_answer():
    data = request.get_json()
    category = data.get("category")
    points = int(data.get("points"))
    user_response = data.get("user_response", "").strip().lower()

    q = Question.query.filter_by(category=category, points=points).first()
    if not q:
        return jsonify({"result": "Clue not found."}), 404

    expected_response = q.response.strip().lower()
    is_correct = expected_response == user_response

    return jsonify({
        "correct": is_correct,
        "expected_response": q.response
    })

if __name__ == "__main__":
    app.run(debug=True)
