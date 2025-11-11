from tinydb import TinyDB, Query

db = TinyDB("db.json")

users_table = db.table("users")
User = Query()

def create_user(username, password):
    existing = users_table.get(User.username == username)
    if existing:
        return {"message": "user already exists!", "status": "error"}

    users_table.insert({"username": username, "password": password, "schedule": [], "viewer_on": []})
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
    return {"message": "Schedule updated successfully!", "status": "success"}

def get_schedule(username):

    user = users_table.get(User.username == username)
    
    if not user:
        print("User not found")
        return None
    
    sch = user.get('schedule', [])

    return sch

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
    
    
