# File for controlling viewers
from db_utils import get_schedule
from gemini_utils import generate_output

# Triggered when the user select yes
# Send auto notification to the selected viewers
# Situation:
# 1. Activity changed for the selected viewers 
# 2. New suggested activity generated for getting together
def auto_notification():
    print()