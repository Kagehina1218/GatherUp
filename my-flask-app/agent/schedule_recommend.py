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
            Return the recommendations in a friendly, clear way.
        '''
    )

    return prompt

def schedule_recommend(username):
    schedule = get_schedule(username)
    prompt = recommend_prompt(schedule)
    output = generate_output(prompt)
    return output