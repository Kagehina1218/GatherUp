from db_utils import get_schedule
from gemini_utils import generate_output

def recommend_prompt(schedule):
    prompt = (
        "You are an AI scheduling assistant. Below is a list of user's current schedule: \n\n"
    )

    for activity in schedule:
        description = activity.get("Description", "Missing information")
        time = activity.get("Time Period", "Any time")
        number = activity.get("Activity Number", "N/A")

        prompt += (
            f" Activity #{number}: {description}, Time Period: {time}\n"
        )

    prompt += (
        '''
            \nPlease analyze the schedule and recommend an improved daily plan. 
            Considering timing, possible time conflicts, natural day flow, and productivity.
            Return the recommendations in a friendly, clear way.\n
            Turn what the recommendations into a schedule for the day give it in the json format: 
            - "Activity Number" (default to 1, ascending and based on the time allocation)
            - "Description" (what the activity is)
            - "Time Period" (the time it will take place; if a duration is not provided, accept a specific time and assume a number as the time and accept as a string)
        '''
    )

    return prompt

def recommend_friends_prompt(schedule):
    prompt = (
        "You are an AI scheduling assistant. Below is a list of user's current schedule and their friends' schedule: \n\n"
    )

    prompt += (
        "The users's schedule: \n"
    )

    for activity in schedule:
        description = activity.get("Description", "Missing information")
        time = activity.get("Time Period", "Any time")
        number = activity.get("Activity Number", "N/A")

        prompt += (
            f" Activity #{number}: {description}, Time Period: {time}\n"
        )

    prompt += (
        "The their freinds' schedules: \n"
    )

    for activity in schedule:
        description = activity.get("Description", "Missing information")
        time = activity.get("Time Period", "Any time")
        number = activity.get("Activity Number", "N/A")

        prompt += (
            f" Activity #{number}: {description}, Time Period: {time}\n"
        )


    prompt += (
        '''
            \nPlease analyze the schedule and recommend an improved daily hang out time/meeting based on the friend group. 
            Considering timing, possible time conflicts, and natural day flow.
            Return the recommendations in a friendly, clear way.\n
            Turn what the recommendations into a schedule for the day give it in the json format: 
            - "Activity Number" (default to 1, ascending and based on the time allocation)
            - "Description" (what the activity is)
            - "Time Period" (the time it will take place; if a duration is not provided, accept a specific time and assume a number as the time and accept as a string)
        '''
    )

    return prompt

def schedule_recommend(username):
    schedule = get_schedule(username)
    prompt = recommend_prompt(schedule)
    output = generate_output(prompt)
    return output

def meeting_recommend(username):
    schedule = get_schedule(username)
    prompt = recommend_friends_prompt(schedule)
    output = generate_output(prompt)
    return output