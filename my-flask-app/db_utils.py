from tinydb import TinyDB, Query
from mail_utils import send_gmail

db = TinyDB("db.json")

users_table = db.table("users")
User = Query()

def create_user(username, password, email):
    existing = users_table.get(User.username == username)
    if existing:
        return {"message": "user already exists!", "status": "error"}

    users_table.insert({"username": username, "email": email, "password": password, "schedule": [], "viewer_on": []})
    return {"message": "Signup successful!", "status": "success"}


def check_user(username, password):
    existing = users_table.get((User.username == username) & (User.password == password))
    if existing:
        print("Message: username/password found")
        return True
    print("Message: Username/password not found")
    return False

def update_schedule(username, schedule):
    existing = users_table.get(User.username == username)
    
    if not existing:
        return {"message": "User not found", "status": "error"}

    users_table.update({"schedule": schedule}, User.username == username)

    # have to find everyone who is a viewer on __username
    friends = users_to_mail(username)

    message = "Your Friend " + username + "updated their schedule, check now"

    send_gmail(friends, "Gatherup notification", message)

    return {"message": "Schedule updated successfully!", "status": "success"}


def users_to_mail(username):
    results = []
    allUsers = users_table.all()

    for user in allUsers:
        viewerList = user.get("viewer_on", [])
        if username in viewerList:
            results.append(username['email'])
    return results

def add_schedule(username, new_item):
    user = users_table.get(User.username == username)
    if not user:
        return {"message": "User not found", "status": "error"}

    current_schedule = user.get("schedule", [])

    for item in new_item:
        item["Activity Number"] = len(current_schedule) + 1

    current_schedule.extend(new_item)

    users_table.update({"schedule": current_schedule}, User.username == username)

    return {"message": "Schedule item added successfully!", "status": "success"}


def get_schedule(username):

    user = users_table.get(User.username == username)
    
    if not user:
        print("User not found")
        return None
    
    sch = user.get('schedule', [])

    return sch

def get_email(username):

    user = users_table.get(User.username == username)
    
    if not user:
        print("User not found")
        return None
    
    em = user.get('email', "")

    return em

def add_viewer(username, friendUsername):

    if not friendUsername or friendUsername == username:
        return False

    friend = users_table.get(User.username == friendUsername)
    if not friend:
        return False

    viewers_list = friend.get('viewer_on', [])

    if username not in viewers_list:
        viewers_list.append(username)
        users_table.update({'viewer_on': viewers_list}, User.username == friendUsername)

    return True

def viewableFriends(username):
    
    user = users_table.get(User.username == username)
    
    if not user:
        print("User not found")
        return None
    
    friendlist = user.get('viewer_on', [])

    return friendlist
    
def viewableFriendsByGroup(username):
    user = users_table.get(User.username == username)
    if not user:
        return {}
    return user.get("groups", {})

def add_friend_to_group(username, friend_username, group_name):
    user = users_table.get(User.username == username)
    friend = users_table.get(User.username == friend_username)
    
    if not user or not friend or username == friend_username:
        return {"message": "Invalid operation", "status": "error"}

    groups = user.get("groups", {})

    if group_name not in groups:
        groups[group_name] = []

    if friend_username not in groups[group_name]:
        groups[group_name].append(friend_username)
        users_table.update({"groups": groups}, User.username == username)

    return {"message": f"{friend_username} added to group {group_name}", "status": "success"}

