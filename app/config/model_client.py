import google.generativeai as genai
from openai import OpenAI
from config.settings import GOOGLE_API_KEY, OPENAI_API_KEY
import time 


class AIModels:
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model_gemini = genai.GenerativeModel("gemini-1.5-flash")
        self.model_openai = OpenAI(api_key=OPENAI_API_KEY)

    def generate_gemini_response(self, prompt: str):
        """Menghasilkan respons dari Gemini tanpa kontrol temperatur."""
        start_time = time.time()
        try:
            response = self.model_gemini.generate_content([prompt])
            end_time = time.time()

            time_taken = end_time - start_time
            tokens_used = len(response.text.split())
            print(f"Gemini Response Time: {time_taken:.2f} seconds")
            print(f"Gemini Tokens Used: {tokens_used} tokens")

            return (
                response.text.strip()
                if response and hasattr(response, "text")
                else None
            )

        except Exception as e:
            end_time = time.time()
            time_taken = end_time - start_time
            print(f"Gemini Error Response: {e}")
            return "Mohon maaf kakak, saat ini sedang ada maintenance 🙏. Kami sedang memperbaiki masalah dan akan kembali segera. Terima kasih atas pengertiannya! 😊"

    def generate_openai_response(
        self, prompt: str, model="gpt-4", max_tokens=500, temperature=0.8
    ):
        """Menghasilkan respons dari OpenAI (GPT) dengan kontrol temperatur."""
        start_time = time.time()
        try:
            response = self.model_openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            end_time = time.time()

            time_taken = end_time - start_time
            tokens_used = response.usage["total_tokens"]
            print(f"OpenAI Response Time: {time_taken:.2f} seconds")
            print(f"OpenAI Tokens Used: {tokens_used} tokens")

            return (
                response.choices[0].message.content.strip()
                if response.choices
                else None
            )

        except Exception:
            end_time = time.time()
            time_taken = end_time - start_time
            print(f"OpenAI Error Response Time: {time_taken:.2f} seconds")
            return "Mohon maaf kakak, saat ini sedang ada maintenance 🙏. Kami sedang memperbaiki masalah dan akan kembali segera. Terima kasih atas pengertiannya! 😊"

    def get_openai_client(self):
        """Mengembalikan instance OpenAI Client."""
        return self.model_openai

    def generate_response(self, model: str, prompt: any):
        """Pilih model yang tepat (Gemini atau OpenAI) berdasarkan parameter model."""
        openai_model_list = ["gpt-3.5-turbo", "gpt-4"]

        if model in ["gemini-1.5-flash", "gemini-1.5", "gemini-1.0-pro"]:
            return self.generate_gemini_response(prompt)

        elif model in openai_model_list:
            return self.generate_openai_response(model=model, prompt=prompt)

        else:
            return "Mohon maaf kakak, model yang diminta tidak tersedia saat ini 🙏. Silakan coba model lain."
