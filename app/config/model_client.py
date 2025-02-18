import google.generativeai as genai
from openai import OpenAI
import time
from config.settings import GOOGLE_API_KEY, OPENAI_API_KEY


# Fungsi untuk mengonfigurasi model Gemini
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


# Fungsi untuk mengonfigurasi model OpenAI
def configure_openai_model():
    model_openai = OpenAI(api_key=OPENAI_API_KEY)
    return model_openai


# Fungsi untuk menghasilkan respons dari Gemini
def generate_gemini_response(model, prompt: str):
    """Menghasilkan respons dari Gemini tanpa kontrol temperatur."""

    try:
        response = model.generate_content([prompt])

        return response.text.strip() if response and hasattr(response, "text") else None
    except Exception as e:
        print(f"Gemini Error Response: {e}")
        return "Mohon maaf kakak, saat ini sedang ada maintenance 🙏. Kami sedang memperbaiki masalah dan akan kembali segera. Terima kasih atas pengertiannya! 😊"


def generate_openai_response(
    model, prompt: str, model_name="gpt-4", max_tokens=500, temperature=0.8
):
    """Menghasilkan respons dari OpenAI (GPT) dengan kontrol temperatur."""

    try:
        response = model.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        end_time = time.time()

        return response.choices[0].message.content.strip() if response.choices else None
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "Mohon maaf kakak, saat ini sedang ada maintenance 🙏. Kami sedang memperbaiki masalah dan akan kembali segera. Terima kasih atas pengertiannya! 😊"


def generate_response(model: str, prompt: any):
    """Pilih model yang tepat (Gemini atau OpenAI) berdasarkan parameter model."""

    openai_model_list = ["gpt-3.5-turbo", "gpt-4"]

    if model in ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.0-pro"]:
        model_gemini = configure_gemini_model(model=model)
        return generate_gemini_response(model=model_gemini, prompt=prompt)
    elif model in openai_model_list:
        model_openai = configure_openai_model()
        return generate_openai_response(model=model_openai, prompt=prompt)
    else:
        return "Mohon maaf kakak, model yang diminta tidak tersedia saat ini 🙏. Silakan coba model lain."
