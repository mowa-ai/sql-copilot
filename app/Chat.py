import logging

import streamlit as st

from app.chat import callbacks, config, utils
from app.chat.data_models import Message, MessagePayload, MessageType
from app.engine.engine import generate_query
from app.engine.sql_engine import Database

logger = logging.getLogger(__name__)


utils.setup_look("Mowa SQL Copilot")
db = Database()


def chat_interface():
    with st.sidebar:
        st.selectbox(
            "Language",
            ("English", "Polish"),
            key="lang",
            label_visibility="hidden",
            on_change=callbacks.on_lang_change,
        )

        st.markdown("***")
        table_name = st.selectbox(config.LANG_DICT[st.session_state["lang"]]["check_schema"], db.tables)
        _, center, _ = st.columns([0.1, 1, 0.1])
        with center:
            st.dataframe(
                db.schema_dict[table_name],
                hide_index=False,
            )

        with st.expander(config.LANG_DICT[st.session_state["lang"]]["choose_tables"]):
            st.multiselect(
                "Tables",
                db.tables,
                default=db.tables,
                key="chosen_tables",
                label_visibility="hidden",
                on_change=callbacks.on_table_change,
            )

    chat_placeholder = st.empty()
    with chat_placeholder.container():
        with st.chat_message("bot", avatar=utils.URL_TO_ICON):
            st.write(config.LANG_DICT[st.session_state["lang"]]["welcome_msg"])
        utils.show_messages()
        if len(st.session_state[config.HISTORY]) > 0:
            is_active_editor = st.session_state[config.BOT_MESSAGE][-1].payload.active or False
        else:
            is_active_editor = False
        user_input = st.chat_input(
            placeholder=config.LANG_DICT[st.session_state["lang"]]["placeholder"], disabled=is_active_editor
        )
        if user_input:
            logger.debug("on user input")
            st.chat_input(
                placeholder=config.LANG_DICT[st.session_state["lang"]]["placeholder"],
                disabled=True,
                key="disabled_chat_input",
            )
            user_message = Message(
                message_type=MessageType.USER,
                payload=MessagePayload(text=user_input),
            )
            st.session_state[config.USER_MESSAGE].append(user_message)

            with st.chat_message("user"):
                st.write(user_message.payload.text)

            st.info(config.LANG_DICT[st.session_state["lang"]]["sending_msg"])
            query = (
                generate_query(
                    text=user_message.payload.text, history=st.session_state.history, lang=st.session_state["lang"]
                )
                .strip()
                .split(";")[0]
            )

            ai_message = Message(
                message_type=MessageType.AI,
                payload=MessagePayload(code=query, active=True),
            )
            st.session_state.history.append(
                {"type": "Human", "text": user_message.payload.text},
            )
            callbacks.update_session_state_on_response(ai_message)

            st.rerun()

        col1, col2 = st.columns([0.25, 1])
        with col1:
            st.button(config.LANG_DICT[st.session_state["lang"]]["clear_button"], on_click=callbacks.on_clear_click)
        with col2:
            if is_active_editor:
                st.button(
                    config.LANG_DICT[st.session_state["lang"]]["change_button"], on_click=callbacks.on_regen_click
                )


if __name__ == "__main__":
    st.title("Mowa SQL Copilot")
    config.initialize_streamlit()
    chat_interface()
