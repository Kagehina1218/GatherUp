from flask import Flask, render_template, request, jsonify, session, url_for, redirect, session

import json
from db_utils import create_user, check_user, update_schedule, get_schedule
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


@app.route("/mySchedule", methods = ["GET"])
def mySchedule():
    myS = get_schedule(session.get('username')) or ""
    print("trying to get schedule")
    return render_template("schedule.html", mySchedule = myS)

@app.route("/demo" , methods = ["GET", "POST"])
def demo():
    responseText = None

    if request.method == "POST":
        text = nlp()
        print(text)
        
        responseText = None

        if text:
            text += "-->{Turn what I inputed before into a schedule for the day--> give it in the json format: (Activity Number, Description, Time Period)}"

        responseText = generate_schedule(text)
    
        start = responseText.find('[')
        end = responseText.rfind(']')
        schText = responseText[start:end + 1]
        schObj = json.loads(schText)
        
        res = update_schedule(session.get('username'), schObj)
        
        
        print(res, type(res))

    return render_template("demo.html", text = responseText or "")

@app.route("/logout")
def logout():
    session.clear()
    print("user logged out")
    return redirect(url_for('login'))

@app.route("/loginhere", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            result = check_user(username, password)

            print(result)

            if result:
                session['username'] = username
                print("session user: ", session.get('username'))
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
