import google.generativeai as genai
from config.settings import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)
MODEL = genai.GenerativeModel("gemini-1.5-flash")