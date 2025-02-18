import time
import streamlit as st
from services.genai_service import generate_answer_without_embed
from datetime import datetime
from config.meilisearch_client import meiliClient


def initialize_session():
    """Inisialisasi histori percakapan di session state."""
    if "conversations" not in st.session_state:
        st.session_state.conversations = {}
        st.session_state.selected_conversation = None


def type_effect(text, speed=0.1):
    """Efek mengetik teks secara perlahan di Streamlit."""
    text_placeholder = st.empty()
    displayed_text = ""

    for char in text:
        displayed_text += char
        text_placeholder.write(displayed_text)
        time.sleep(speed)


def save_conversation(conversation_id, conversation_history):
    """Simpan percakapan di session state."""
    st.session_state.conversations[conversation_id] = conversation_history


def reset_conversation():
    """Reset percakapan baru di session state."""
    st.session_state.selected_conversation = None


def main():
    """Fungsi utama untuk menjalankan chatbot Kanita di Streamlit."""
    st.title("Kanita Chatbot - PT. Knitto Textile Indonesia")
    st.subheader("Virtual Assistant")

    initialize_session()

    conversation_options = list(st.session_state.conversations.keys())
    conversation_options.append("Percakapan Baru")

    selected_conversation = st.selectbox("Pilih percakapan", conversation_options)

    if selected_conversation == "Percakapan Baru":
        st.session_state.selected_conversation = str(datetime.now())
        st.session_state.conversations[st.session_state.selected_conversation] = []
        st.session_state.first_question = True
        st.session_state.registered_no_hp = ""
        st.session_state.nama = ""
    else:
        st.session_state.selected_conversation = selected_conversation

    conversation_history = st.session_state.conversations[
        st.session_state.selected_conversation
    ]

    registered_no_hp = st.text_input("Masukkan nomor HP terdaftar Anda:")

    if registered_no_hp:
        st.session_state.registered_no_hp = registered_no_hp
        
        index = meiliClient.index("customer")
        filter_cond = f"""no_hp = '{registered_no_hp}'"""
        results = index.search("", {"limit": 1, "filter": filter_cond})
        nama_customer = results['hits'][0]['nama_customer']
        st.session_state.nama = nama_customer
        
        if nama_customer:
            st.success(f"Selamat datang, Kak {nama_customer} 😊")
        else:
            st.success(f"Nomor HP terdaftar: {registered_no_hp}")

    question = st.text_input("Masukkan pertanyaan Anda:")

    if question:
        if registered_no_hp:
            answer = generate_answer_without_embed(
            question, st.session_state.first_question, nohp=registered_no_hp,
            nama_customer=st.session_state.nama
        )
    
        conversation_history.append({"user": question, "kanita": answer})

        st.session_state.first_question = False

        st.write("Jawaban dari Kanita:")
        type_effect(answer, speed=0.01)

    st.subheader("Riwayat Percakapan:")
    for chat in reversed(conversation_history):
        st.text(f"🧑 : {chat['user']}")
        st.text(f"🤖 : {chat['kanita']}")

    if st.button("Mulai Percakapan Baru"):
        reset_conversation()
        st.success("Percakapan baru telah dimulai!")


if __name__ == "__main__":
    main()
