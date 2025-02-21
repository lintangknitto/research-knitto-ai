import google.generativeai as genai
from openai import OpenAI
import time
from config.settings import GOOGLE_API_KEY, OPENAI_API_KEY


def configure_gemini_model(
    model="gemini-1.5-flash", temperature=1, top_p=0.95, top_k=40, max_tokens=8192
):
    genai.configure(api_key=GOOGLE_API_KEY)

    generation_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_tokens,
        "response_mime_type": "text/plain",
    }

    model_gemini = genai.GenerativeModel(
        model_name=model,
        generation_config=generation_config,
    )
    return model_gemini


def configure_openai_model():
    model_openai = OpenAI(api_key=OPENAI_API_KEY)
    return model_openai
