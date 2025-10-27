import google.generativeai as genai

API_KEY = None
if not API_KEY:
    raise ValueError("Google API key not set yet")

genai.configure(api_key=API_KEY)


def generate_schedule(prompt):
            model = genai.GenerativeModel('gemini-2.5-flash-lite')
            response = model.generate_content(prompt)
            return response.text
