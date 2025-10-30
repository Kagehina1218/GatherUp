from flask import Flask, render_template, request, jsonify, session, url_for

import json
from db_utils import create_user
from gemini_utils import generate_schedule


app = Flask(__name__)
app.secret_key = "secretKey222"

@app.route("/", methods = ["GET"])
def home():
    username = "kain"
    password = "johnson"

    result = create_user(username, password)
    print(result)

    return render_template("login.html")

@app.route("/demo" , methods = ["GET"])
def demo():
    responseText = generate_schedule("give me a json response with a random schedule in less than 100 words")

    return render_template("demo.html", text = responseText or "")

@app.route("/loginhere", methods = ["POST"])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        result = create_user(username, password)

        print (result)

        
    except Exception as e:
        print(e)
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
