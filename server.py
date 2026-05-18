from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="raghava@1438",
    database="online_exam"
)

cursor = db.cursor()

@app.route("/")
def home():
    return "Online Exam Backend Running"


# Save exam result
@app.route("/submit_exam", methods=["POST"])
def submit_exam():

    data = request.get_json()

    name = data.get("name")
    course = data.get("course")
    year = data.get("year")
    score = data.get("score")

    cursor.execute(
        "INSERT INTO results(name,course,year,score) VALUES(%s,%s,%s,%s)",
        (name, course, year, score)
    )

    db.commit()

    return jsonify({"message": "Result saved successfully"})


# Get student results for dashboard
@app.route("/students", methods=["GET"])
def students():

    cursor.execute("SELECT name,course,year,score FROM results")

    rows = cursor.fetchall()

    students_list = []

    for r in rows:
        students_list.append({
            "name": r[0],
            "course": r[1],
            "year": r[2],
            "score": r[3]
        })

    return jsonify(students_list)


app.run(host="0.0.0.0", port=5000, debug=True)