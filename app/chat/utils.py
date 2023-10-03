import base64
import logging
from pathlib import Path

import pandas as pd
import sqlparse
import streamlit as st
from code_editor import code_editor
from PIL import Image

from app.chat import callbacks, config
from app.chat.data_models import Message, MessagePayload, MessageType
from app.engine.engine import execute_query

logger = logging.getLogger(__name__)
URL_TO_ICON = "https://storage.googleapis.com/assets_mvp/Icon.png"
pd.options.display.float_format = "{:.2f}".format


code_buttons = [
    {
        "name": "Run",
        "feather": "Play",
        "alwaysOn": True,
        "primary": True,
        "hasText": True,
        "showWithIcon": True,
        "commands": ["submit"],
        "style": {"bottom": "0.44rem", "right": "0.4rem"},
    },
]


def setup_look(
    page_title,
    icon_path="imgs/Icon.png",
):
    im = Image.open(icon_path)
    st.set_page_config(page_title=page_title, page_icon=im, initial_sidebar_state="expanded")
    hide_footer_style = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
    st.markdown(hide_footer_style, unsafe_allow_html=True)


def run_code_editor(sql_code):
    response_dict = code_editor(
        sql_code,
        lang="sql",
        buttons=code_buttons,
        focus=True,
    )

    if response_dict["type"] == "submit" and len(response_dict["text"]) != 0:
        try:
            df = execute_query(response_dict["text"])
            df = df.loc[:, ~df.columns.duplicated()]
            st.dataframe(df, hide_index=True)
        except Exception as exeption:
            st.write(str(exeption))
            return

        ai_message = Message(
            message_type=MessageType.AI,
            payload=MessagePayload(code=response_dict["text"], df=df, active=False),
        )
        callbacks.update_session_state_on_response(ai_message, update=True)
        response_dict = None
        st.rerun()


def show_bot_message(msg: Message, active: bool) -> None:
    if msg.payload.code or msg.payload.text:
        with st.chat_message("bot", avatar=URL_TO_ICON):
            if msg.payload.text:
                st.write(msg.payload.text)
            if msg.payload.code:
                sql_code = sqlparse.format(msg.payload.code, reindent=True, keyword_case="upper")
                if active:
                    run_code_editor(sql_code)
                else:
                    st.code(sql_code, language="sql")
                if msg.payload.df is not None:
                    st.dataframe(
                        msg.payload.df,
                        hide_index=True,
                    )


def show_messages() -> None:
    messages = st.session_state[config.BOT_MESSAGE] + st.session_state[config.USER_MESSAGE]
    messages.sort(key=lambda x: x.timestamp)
    for msg in messages:
        if msg.message_type == MessageType.AI:
            show_bot_message(msg, msg.payload.active)
        else:
            with st.chat_message("user"):
                st.write(msg.payload.text)
