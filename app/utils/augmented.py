from config.model_client import configure_gemini_model, configure_openai_model

def generate_gemini_response(model, prompt: str):
    """Menghasilkan respons dari Gemini tanpa kontrol temperatur."""

    try:
        response = model.generate_content([prompt])

        print(response.usage_metadata)
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

        return response.choices[0].message.content.strip() if response.choices else None
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "Mohon maaf kakak, saat ini sedang ada maintenance 🙏. Kami sedang memperbaiki masalah dan akan kembali segera. Terima kasih atas pengertiannya! 😊"


def generate_response(model: str, prompt: any, id: str):
    openai_model_list = ["gpt-3.5-turbo", "gpt-4"]
    gemini_model_list = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.0-pro"]
    
    print('PROCESSS ID : ', id)
    if model in gemini_model_list:
        model_gemini = configure_gemini_model(model=model)
        return generate_gemini_response(model=model_gemini, prompt=prompt)
    elif model in openai_model_list:
        model_openai = configure_openai_model()
        return generate_openai_response(model=model_openai, prompt=prompt)
    else:
        return "Mohon maaf kakak, model yang diminta tidak tersedia saat ini 🙏. Silakan coba model lain."
