from db_utils import get_schedule, viewableFriends, getFriendsSchedule
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
        prompt += "Friends' schedules:\n"
        for f in friends:
            for name, fschedule in f.items():
                prompt += f"  {name}: {fschedule}\n"


    prompt += (
    '''
    Your task:\n
    1. Analyze the user's current schedule and suggest improvements for better time management, considering productivity, natural day flow, and avoiding overlaps.\n
    2. Identify free time slots and overlapping activities.\n
    3. Suggest new meeting times during free periods, considering the schedules of the user's friends.\n
    4. If a time period is vague (e.g., 'morning', 'afternoon', 'evening', 'night'), convert it into a specific start and end time using common daily conventions.\n
    5. Ensure that suggested meetings and improved schedule items do not conflict with existing activities.\n
    6. For meetings involving friends, include them in a "Participants" list. For personal activities, "Participants" can be empty.\n
    \n
    Output format:\n
    - Return a structured list of activities and suggested meetings in JSON format only.\n
    - Each activity or meeting should have:\n
      - "Activity Number": starting at 1, ascending, ordered by time\n
      - "Description": a short explanation of the activity or meeting\n
      - "Time Period": start time and end time as a single string (e.g., "7:00 AM - 8:00 AM")\n
      - "Participants": list of friends participating (empty if personal activity)\n
    - Do not include extra commentary, explanations, or text outside the JSON.\n
    - Every item **must include** all four fields: "Activity Number", "Description", "Time Period", and "Participants".\n
    \n
    Example output:\n
    [\n
      {\n
        "Activity Number": 1,\n
        "Description": "Morning walk",\n
        "Time Period": "7:00 AM - 8:00 AM",\n
        "Participants": []\n
      },\n
      {\n
        "Activity Number": 2,\n
        "Description": "Team meeting",\n
        "Time Period": "10:00 AM - 11:00 AM",\n
        "Participants": ["alice", "bob"]\n
      },\n
      {\n
        "Activity Number": 3,\n
        "Description": "Lunch break",\n
        "Time Period": "12:00 PM - 1:00 PM",\n
        "Participants": []\n
      }\n
    ]\n
    \n
    Return only valid JSON, using double quotes for all keys and strings.\n
    '''
    )
    return prompt

def schedule_recommend(username):
    schedule = get_schedule(username)
    friendList = viewableFriends(username)
    fSchedule = []
    for aFriend in friendList:
        fSchedule.append({aFriend: get_schedule(aFriend)})
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
