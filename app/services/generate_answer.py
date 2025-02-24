from app.utils.intent_detection import detect_intent
from app.utils.prompt_generator_v2 import prompt_generator
from app.utils.augmented import generate_response
from app.utils.logger import write_log
import time
import json
from datetime import datetime


async def generate_answer(
    id_log: str, question: str, first: bool, nohp: str, nama_customer: str
):
    epoch_time = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())
    start_time = time.time()

    # Mendeteksi intent dari pertanyaan
    intent = detect_intent(question=question)
    print("INTENT TERDETEKSI : ", intent)

    # Membuat prompt untuk mengirim ke model
    result_prompt = prompt_generator(
        question=question,
        intent=intent,
        no_hp=nohp,
        first_chat=first,
        first_intent=intent,
        nama_customer=nama_customer,
    )

    # Parsing hasil prompt yang didapatkan
    response_prompt = json.loads(result_prompt)

    try:
        # Menghasilkan response dari model (Gemini)
        response = generate_response(
            model="gemini-2.0-flash",
            prompt=response_prompt["prompt"],
            id="GENERATE CHAT",
        )

        response_json = json.loads(response)

        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        print("RESPONSE TIME: ", response_time)

        return response_json["response_content"]

    except Exception as e:
        return f"Error 2: {e}"

    finally:
        if "response_json" in locals() and "response_time" in locals():
            await write_log(
                id=id_log,
                question=question,
                answer=response_json.get("response_content", "No content"),
                response_time=response_time,
                intent=intent,
                context=response_prompt.get("context", ""),
                nohp=nohp,
                level="INFO",
                usage_metadata=response_json.get("usage_metadata", {}),
                date=epoch_time,
            )
