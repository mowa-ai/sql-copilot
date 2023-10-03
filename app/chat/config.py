import logging
import uuid

import streamlit as st

logger = logging.getLogger(__name__)

USER_MESSAGE = "user_message"
BOT_MESSAGE = "bot_message"
HISTORY = "history"
LANG_DICT = {
    "English": {
        "check_schema": "Check schema",
        "choose_tables": "Tables for assistant",
        "placeholder": "Your message",
        "clear_button": "Clear messages",
        "change_button": "Change request",
        "sending_msg": "Sending message to AI...",
        "welcome_msg": """
Hello! I'm MowaSQL, a computer-based SQL Copilot created by [mowaAI](https://www.mowa.ai/). Visit my creators' webpage and don't hesitate to reach them.

I'm designed to understand text in natural language and translate it to SQL, which means I can assist you in analyzing various datasets. Ask a question, check SQL code I've generated, edit if necessary and run to get a result.

What would you like to ask?
""",
    },
    "Polish": {
        "check_schema": "Sprawdź schemat",
        "choose_tables": "Tabele dla Asystenta",
        "placeholder": "Twoja wiadomość",
        "clear_button": "Wyczyść",
        "change_button": "Zmień zapytanie",
        "sending_msg": "Wysyłanie wiadomości do AI...",
        "welcome_msg": """
Cześć! Jestem MowaSQL, twój personalny SQL Copilot, stworzony przez [mowaAI](https://www.mowa.ai/). Odwiedź stronę internetową moich twórców i nie wahaj się z nimi skontaktować.

Jestem stworzony do rozumienia tekstu w języku naturalnym i tłumaczenia go na SQL, co oznacza, że mogę pomóc Ci w analizie różnych zbiorów danych. Zadaj pytanie, sprawdź wygenerowany kod SQL, w razie potrzeby edytuj i uruchom, aby uzyskać wynik.

O co chciałbyś zapytać?
""",
    },
}


def initialize_streamlit() -> None:
    st.session_state.setdefault(USER_MESSAGE, [])
    st.session_state.setdefault("lang", "English")
    st.session_state.setdefault(BOT_MESSAGE, [])
    st.session_state.setdefault(HISTORY, [])
    st.session_state.setdefault("chat_id", uuid.uuid4().hex)
    st.session_state.setdefault("tables", uuid.uuid4().hex)
