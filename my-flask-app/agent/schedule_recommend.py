from db_utils import get_schedule, viewableFriends, getFriendsSchedule, get_friend_groups
from gemini_utils import generate_output
from mail_utils import send_gmail
import json
import re

def recommend_prompt(schedule, friends):
    prompt = (
        "You are an AI scheduling assistant. Below is a list of user's current schedule: \n\n"
    )

    prompt += (
        "User's schedule is listed as: \n\n"
    )

    for activity in schedule:
        description = activity.get("Description", "Missing information")
        time = activity.get("Time Period", "Any time")
        number = activity.get("Activity Number", "N/A")

        prompt += (
            f" Activity #{number}: {description}, Time Period: {time}\n"
        )

    if friends:
        prompt += "Friends' schedules and groups:\n"
        for f in friends:
            name = f["name"]
            schedule = f["schedule"]
            groups = f["groups"]

        prompt += f"- {name} (Groups: {groups}):\n"
        prompt += f"  Schedule: {schedule}\n"


    prompt += (
    '''
        Your task:

        Analyze the user's schedule and generate an improved version of their day.

        Instructions:
        1. Analyze the user's current schedule and suggest improvements for better time management, considering productivity, natural day flow, and avoiding overlaps.
        2. Identify free time slots and overlapping activities.
        3. Suggest new meeting times during free periods, considering the schedules of the user's friends.
        4. If a time period is vague (e.g., "morning", "afternoon", "evening", "night"), convert it into a specific start and end time using common daily conventions.
        5. Ensure that suggested meetings and improved schedule items do not conflict with existing activities.
        6. For meetings involving friends, include them in a "Participants" list. For personal activities, use an empty list.
        7. Consider the friend's group when suggesting meeting types:

        Group guidelines:
        - "Close Friends": suggest casual hangouts, meals, personal activities.
        - "Gym Buddies": suggest workouts, exercise sessions, or sports activities.
        - "Family": suggest family-friendly or home-oriented activities.
        - If multiple groups apply, choose the most suitable for the time slot or activity.
        - - If the group name is not listed in the guidelines, give a reasonable meeting recommendation based on common sense and the name of the group.

        Output format:

        - Return a structured list in **JSON only**.
        - Each item must include:
        - "Activity Number": starting at 1, ascending by time.
        - "Description": short explanation of the activity or meeting.
        - "Time Period": formatted as "Start Time - End Time".
        - "Participants": list of involved friends (or empty list).

        Do not include explanations outside of the JSON.
        Only return valid JSON with double quotes for all keys and strings.

        Example output:
        [
        {
            "Activity Number": 1,
            "Description": "Morning walk",
            "Time Period": "7:00 AM - 8:00 AM",
            "Participants": []
        },
        {
            "Activity Number": 2,
            "Description": "Team meeting",
            "Time Period": "10:00 AM - 11:00 AM",
            "Participants": ["alice", "bob"]
        },
        {
            "Activity Number": 3,
            "Description": "Lunch break",
            "Time Period": "12:00 PM - 1:00 PM",
            "Participants": []
        }
        ]
        '''
)
    return prompt

def schedule_recommend(username):
    schedule = get_schedule(username)
    friendList = viewableFriends(username)
    friendGroup = get_friend_groups(username)
    fSchedule = []
    for aFriend in friendList:
        fSchedule.append({
            "name": aFriend,
            "schedule": get_schedule(aFriend),
            "groups": friendGroup.get(aFriend, [])
        })
    prompt = recommend_prompt(schedule, fSchedule)
    output = generate_output(prompt)
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        match = re.search(r"\[\s*{.*}\s*\]", output, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        print("Not valid JSON from AI output:")
        print(output)
        return []
