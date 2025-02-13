import time
import streamlit as st
from services.genai_service import generate_answer_without_embed


def initialize_session():
    """Inisialisasi histori percakapan di session state."""
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
        st.session_state.first_question = True


def type_effect(text, speed=0.1):
    """Efek mengetik teks secara perlahan di Streamlit."""
    text_placeholder = st.empty()
    displayed_text = ""

    for char in text:
        displayed_text += char
        text_placeholder.write(displayed_text)
        time.sleep(speed)


def main():
    """Fungsi utama untuk menjalankan chatbot Kanita di Streamlit."""
    st.title("Kanita Chatbot - PT. Knitto Textile Indonesia")
    st.subheader("Virtual Assistant")

    initialize_session()

    question = st.text_input("Masukkan pertanyaan Anda:")

    if question:
        answer = generate_answer_without_embed(
            question, st.session_state.first_question
        )

        st.session_state.conversation_history.append(
            {"user": question, "kanita": answer}
        )

        st.session_state.first_question = False

        # Menampilkan jawaban dari Kanita
        st.write("Jawaban dari Kanita:")
        type_effect(answer, speed=0.01)

    st.subheader("Riwayat Percakapan:")
    for chat in reversed(st.session_state.conversation_history):
        st.text(f"🧑 : {chat['user']}")
        st.text(f"🤖 : {chat['kanita']}")


if __name__ == "__main__":
    main()
