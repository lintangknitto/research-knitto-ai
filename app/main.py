import time
import streamlit as st
from services.genai_service import generate_answer_without_embed
from datetime import datetime
from config.meilisearch_client import meiliClient


def initialize_session():
    """Inisialisasi histori percakapan di session state."""
    if 'conversations' not in st.session_state:
        st.session_state.conversations = {}
        st.session_state.selected_conversation = None
        st.session_state.first_question = True
        st.session_state.registered_no_hp = ''
        st.session_state.nama = ''
        st.session_state.hp_history = []


def type_effect(text, speed=0.01):
    """Efek mengetik teks secara perlahan di Streamlit."""
    text_placeholder = st.empty()
    displayed_text = ''

    for char in text:
        displayed_text += char
        text_placeholder.markdown(displayed_text)
        time.sleep(speed)


def reset_conversation():
    """Inisialisasi percakapan baru di session state."""
    st.session_state.selected_conversation = str(datetime.now())
    st.session_state.conversations[st.session_state.selected_conversation] = []
    st.session_state.first_question = True


def main():
    """Fungsi utama untuk menjalankan chatbot Kanita di Streamlit."""
    st.set_page_config(page_title="Kanita Chatbot", page_icon="🤖", layout="wide")

    initialize_session()

    with st.sidebar:
        st.logo(image="https://knitto.co.id/assets/svg/logoKnittoCircle.svg", size="small")


        registered_no_hp = st.text_input("No Hp", value=st.session_state.registered_no_hp, placeholder="+62")

        if registered_no_hp:
            st.session_state.registered_no_hp = registered_no_hp
            if registered_no_hp not in st.session_state.hp_history:
                st.session_state.hp_history.append(registered_no_hp)
            index = meiliClient.index("customer")
            filter_cond = f"no_hp = '{registered_no_hp}'"
            results = index.search("", {"limit": 1, "filter": filter_cond})
            try:
                st.session_state.nama = results['hits'][0]['nama_customer']
                st.success(f"Selamat datang, Kak {st.session_state.nama} 😊")
            except (KeyError, IndexError):
                st.session_state.nama = ''
                st.warning(f"Nomor HP terdaftar: {registered_no_hp}")
        

    if st.session_state.selected_conversation is None:
        reset_conversation()

    conversation_history = st.session_state.conversations[st.session_state.selected_conversation]

   

    # Membuat area chat yang bisa discroll
    chat_container = st.container()
    with chat_container:
        st.title("Kanita Chatbot - PT. Knitto Textile Indonesia")
        st.caption("Selamat datang di Virtual Assistant Kanita chatbot, anda bisa bertanya mengenai hal : ")
        st.caption('''
        <ul>
            <li>Status order</li>
            <li>No resi</li>
            <li>Price list</li>
            <li>Stok </li>
            <li>Faq</li>
        </ul>''',unsafe_allow_html =True)
        for chat in conversation_history:
            with st.chat_message("user"):
                st.write(chat['user'])
            with st.chat_message("assistant"):
                st.write(chat['kanita'])

    question = st.chat_input("Masukkan pertanyaan Anda:")

    if question:
        answer = generate_answer_without_embed(
            question,
            st.session_state.first_question,
            nohp=st.session_state.registered_no_hp,
            nama_customer=st.session_state.nama
        )
        conversation_history.append({"user": question, "kanita": answer})
        st.session_state.first_question = False

        with chat_container:
            with st.chat_message("user"):
                st.write(question)
            with st.chat_message("assistant"):
                type_effect(answer, speed=0.01)


if __name__ == "__main__":
    main()
