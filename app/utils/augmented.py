import json
from app.config.model_client import configure_gemini_model, configure_openai_model


# Fungsi untuk menghasilkan respons dari Gemini
def generate_gemini_response(model, prompt: str):
    """Menghasilkan respons dari Gemini tanpa kontrol temperatur."""
    try:
        # Memanggil model Gemini untuk menghasilkan konten
        response = model.generate_content([prompt])

        # Menyusun metadata penggunaan token
        usage_metadata = {
            "prompt_token_count": response.usage_metadata.prompt_token_count,
            "completion_token_count": response.usage_metadata.candidates_token_count,
            "total_token_count": response.usage_metadata.total_token_count,
        }

        # Membentuk hasil dalam bentuk JSON
        result = {
            "response_content": (
                response.text.strip()
                if response and hasattr(response, "text")
                else None
            ),
            "usage_metadata": usage_metadata,
        }

        result_json = json.dumps(result, ensure_ascii=False)

        return result_json

    except Exception as e:
        print(f"Gemini Error Response: {e}")
        return json.dumps(
            {
                "response_content": "Mohon maaf kakak, saat ini sedang ada maintenance 🙏. Kami sedang memperbaiki masalah dan akan kembali segera. Terima kasih atas pengertiannya! 😊"
            },
            ensure_ascii=False,
        )


# Fungsi untuk menghasilkan respons dari OpenAI (GPT)
def generate_openai_response(
    model, prompt: str, model_name="gpt-4", max_tokens=500, temperature=0.8
):
    """Menghasilkan respons dari OpenAI (GPT) dengan kontrol temperatur dan melacak penggunaan token."""
    try:
        response = model.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        response_content = (
            response.choices[0].message.content.strip() if response.choices else None
        )

        # Menyusun metadata penggunaan token
        token_usage = response.usage
        usage_metadata = {
            "prompt_token_count": token_usage.prompt_tokens,
            "completion_token_count": token_usage.completion_tokens,
            "total_token_count": token_usage.total_tokens,
        }

        result = {
            "response_content": response_content,
            "usage_metadata": usage_metadata,
        }

        result_json = json.dumps(result, ensure_ascii=False)

        return result_json

    except Exception as e:
        print(f"OpenAI Error: {e}")
        return json.dumps(
            {
                "response_content": "Mohon maaf kakak, saat ini sedang ada maintenance 🙏. Kami sedang memperbaiki masalah dan akan kembali segera. Terima kasih atas pengertiannya! 😊"
            },
            ensure_ascii=False,
        )


def generate_response(model: str, prompt: any, id: str):
    """Menentukan model mana yang akan dipakai dan mengembalikan respons dalam format JSON."""
    openai_model_list = ["gpt-3.5-turbo", "gpt-4"]
    gemini_model_list = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.0-pro"]

    print("PROCESS ID:", id)

    if model in gemini_model_list:
        model_gemini = configure_gemini_model(model=model)
        return generate_gemini_response(model=model_gemini, prompt=prompt)

    elif model in openai_model_list:
        model_openai = configure_openai_model()
        return generate_openai_response(model=model_openai, prompt=prompt)

    else:
        return json.dumps(
            {
                "response_content": "Mohon maaf kakak, model yang diminta tidak tersedia saat ini 🙏. Silakan coba model lain."
            },
            ensure_ascii=False,
        )
