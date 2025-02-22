from utils.intent_detection import detect_intent
from utils.prompt_generator_v2 import prompt_generator
from utils.augmented import generate_response
import time

def generate_answer(question: str, first: bool, nohp: str, nama_customer: str):
    start_time = time.time()
    
    intent = detect_intent(question=question)
    print('INTENT TERDETEKSI : ', intent)
    
    prompt = prompt_generator(question=question, intent=intent, no_hp=nohp, first_chat=first, first_intent=intent, nama_customer=nama_customer)
    
    try:
        response = generate_response(model="gemini-2.0-flash", prompt=prompt, id='GENERATE CHAT')
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        print('RESPONSE TIME: ', response_time)
        return response
    except Exception as e:
        return f"Error 2: {e}"

