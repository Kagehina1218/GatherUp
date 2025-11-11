from flask import Flask, render_template, request, jsonify, session, url_for, redirect

import json
from db_utils import create_user, check_user
from gemini_utils import generate_schedule
from nlp_utils import nlp

app = Flask(__name__)
app.secret_key = "secretKey222"

@app.route("/", methods = ["GET"])
def home():
    # username = "kain"
    # password = "johnson"

    # result = create_user(username, password)
    # print(result)

    return render_template("login.html")

@app.route("/demo" , methods = ["GET", "POST"])
def demo():
    responseText = None

    if request.method == "POST":
        text = nlp()
        print(text)
        responseText = generate_schedule(text)

    return render_template("demo.html", text = responseText or "")

# Route to login page
@app.route("/loginhere", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            result = check_user(username, password)

            print (result)

            if result:
                return redirect(url_for('demo'))
            

            
        except Exception as e:
            print(e)
     
    return redirect(url_for('home'))

@app.route("/signup", methods = ["POST", "GET"])
def signup():
    print("inside signup")
    
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            result = create_user(username, password)

            print("inside post--", result)

            return redirect(url_for('demo'))
            
        except Exception as e:
            print(e)
    
    return render_template('signup.html')

# Route to Friends page
@app.route("/friends", methods = ["POST", "GET"])
def friends():
    print("inside friend page")
    return render_template('friends.html')

@app.route("/calendar", methods = ["POST", "GET"])
def calendar():
    print("inside calendar page")
    return render_template('calendar.html')

if __name__ == "__main__":
    app.run(debug=True)
