import streamlit as st
from app.services.intent_service import detect_intent
from app.services.generative_service import generate_answer_async

def main():
    st.title("Kanita Chatbot - PT. Knitto Textile Indonesia")
    st.subheader("Virtual Assistant")

    question = st.text_input("Masukkan pertanyaan Anda:")

    if question:
        answer = generate_answer_async(question)
        st.write("Jawaban dari Kanita:")
        st.success(answer)

if __name__ == "__main__":
    main()
