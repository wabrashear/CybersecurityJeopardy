import csv
from app import app, db, Question

with app.app_context():
    db.drop_all()
    db.create_all()

    with open("questions.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = Question(
                category=row["category"],
                points=int(row["points"]),
                clue=row["clue"],
                response=row["response"]
            )
            db.session.add(question)

    db.session.commit()
    print("Database initialized from CSV.")
