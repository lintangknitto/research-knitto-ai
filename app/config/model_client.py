import google.generativeai as genai
import openai
from config.settings import GOOGLE_API_KEY, OPENAI_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)
MODEL = genai.GenerativeModel("gemini-1.5-flash")

openai.api_key = OPENAI_API_KEY

MODEL_OPEN_AI = openai