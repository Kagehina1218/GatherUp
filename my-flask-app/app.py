from flask import Flask, render_template, request, jsonify, session, url_for, redirect, session
from mail_utils import config_mail
import json
from db_utils import create_user, check_user, update_schedule, get_schedule, add_viewer, viewableFriends, add_friend_to_group, viewableFriendsByGroup, add_schedule, get_email
from gemini_utils import generate_output
from nlp_utils import nlp
from agent.schedule_recommend import schedule_recommend

import speech_recognition as sp

app = Flask(__name__)
app.secret_key = "secretKey222"

config_mail(app)

@app.route("/", methods = ["GET"])
def home():
    return render_template("login.html")

@app.route("/mySchedule", methods = ["GET"])
def mySchedule():
    myS = get_schedule(session.get('username')) or ""
    print("trying to get schedule")
    return render_template("schedule.html", mySchedule = myS)

@app.route("/agent", methods = ["GET"])
def agent():
    return render_template("agent.html")

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
            email = request.form.get('email')

            result = create_user(username, password, email)

            print("inside post--", result)

            session['username'] = username
            print("session user: ", session.get('username'))

            return redirect(url_for('demo'))
            
        except Exception as e:
            print(e)
    
    return render_template('signup.html')


@app.route("/addViewer", methods = ["POST"])
def addViewer():
    if request.method == "POST":
        try: 
            user = session.get('username')
            friend = request.form.get('friend')

            if user == friend:
                print("can't add yourself")
                return redirect(url_for('demo'))
            
            result = add_viewer(user, friend)

            if result:
                print("Added Viewer")    
                return redirect(url_for('friends'))
            print("Didn't add the viewer")  

            return redirect(url_for('demo'))
              
        except Exception as e:
            print(e)
    
    print("inside friend page")
    return redirect(url_for('demo'))

@app.route("/friends", methods = ["GET"])
def friends():
    username = session.get("username")
    if not username:
        return redirect(url_for("home"))
    
    selected_group = request.args.get("group", None)

    friend_groups = viewableFriendsByGroup(username) 

    if selected_group and selected_group in friend_groups:
        group_friends = friend_groups[selected_group]
    else:
        group_friends = viewableFriends(username) or []

    return render_template(
        "friends.html",
        friendGroups=friend_groups,
        selectedGroup=selected_group,
        friendList=group_friends
    )

@app.route("/friend_schedule/<friend_username>", methods = ["GET"])
def friend_schedule(friend_username):
    if not viewableFriends(session.get('username')):
        print("Not allowed")
        return redirect(url_for("friends"))
        
    if friend_username in viewableFriends(session.get("username")):
        myS = get_schedule(friend_username) or ""
        print("trying to get schedule")
        return render_template("schedule.html", mySchedule = myS)
    print("Not allowed")
    return redirect(url_for("friends"))

@app.route("/demo", methods=["GET", "POST"])
def demo():
    user = session.get('username')
    schedule = get_schedule(user) or []
    responseText = None
    prompt = """{Turn what I inputed before into a schedule for the day
                   give it in the json format: 
                   - "Activity Number" (optional; if not provided in the input, default to 1)
                   - "Description" (what the activity is)
                   - "Time Period" (the time it will take place; if a duration is not provided, accept a specific time and assume a number as the time and accept as a string)
                If the information I provide is insufficient to create a schedule, respond with: "Wrong".}
            """
    if request.method == "POST":
        username = session.get('username')
        item = request.form.get("schedule_item", "")
        print("item was: ", repr(item))
        if item == "":
            text = nlp()
            if text:
                print('inside if')
                text += prompt
                responseText = generate_output(text)
                start = responseText.find('[')
                end = responseText.rfind(']')
                
                print("gemeni response: ", responseText)
                if responseText == 'Wrong' or start == -1 or end == -1:
                    print("Invalid schedule format received.")
                else:
                    schText = responseText[start:end + 1]
                    try:
                        schObj = json.loads(schText)
                        add_schedule(username, schObj)
                    
                        return redirect(url_for("schedule"))
                    except json.JSONDecodeError:
                        print("Error decoding JSON.")
        else:
            print("inside else")
            text = item
            text += prompt
            responseText = generate_output(text)
            start = responseText.find('[')
            end = responseText.rfind(']')
                
            print("gemeni response: ", responseText)
            if responseText == 'Wrong' or start == -1 or end == -1:
                print("Invalid schedule format received.")
            else:
                schText = responseText[start:end + 1]
                try:
                    schObj = json.loads(schText)
                    add_schedule(username, schObj)
                    return redirect(url_for("schedule"))
                except json.JSONDecodeError:
                    print("Error decoding JSON.")


    return render_template("demo.html", mySchedule=schedule, text=responseText or "")

@app.route("/schedule")
def schedule():
    user = session.get('username')
    schedule = get_schedule(user) or []
    return render_template("schedule.html", mySchedule=schedule)


@app.route("/addViewer", methods=["POST"])
def add_viewer_route():
    user = session.get('username')
    friend = request.form.get("friend")
    print("woring add viewer?")
    if add_viewer(user, friend):
        message = f"{friend} added as viewer."
    else:
        message = "Could not add friend."

    return redirect(url_for("schedule"))
@app.route("/recommend", methods=["GET"])
def recommend():
    username = request.args.get("username")
    output = schedule_recommend(username)
    return jsonify({"recommendation": output})

if __name__ == "__main__":
    app.run(debug=True)