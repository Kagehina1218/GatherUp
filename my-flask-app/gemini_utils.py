import google.generativeai as genai
from dotenv import load_dotenv
import os 

load_dotenv()


API_KEY = os.getenv("GOOGLE_API_KEY") 

if not API_KEY:
    raise ValueError("Google API key not set yet")

genai.configure(api_key=API_KEY)

def generate_output(prompt):
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    response = model.generate_content(prompt)
    return response.text
