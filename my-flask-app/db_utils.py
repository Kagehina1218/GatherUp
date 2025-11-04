from tinydb import TinyDB, Query

db = TinyDB("db.json")

users_table = db.table("users")
User = Query()

def create_user(username, password):
    existing = users_table.get(User.username == username)
    if existing:
        return {"message": "user already exists!", "status": "error"}

    users_table.insert({"username": username, "password": password, "schedule": []})
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
