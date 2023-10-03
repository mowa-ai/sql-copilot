import logging
import uuid

import streamlit as st

from app.chat import config
from app.chat.data_models import Message
from app.engine.sql_engine import Database

logger = logging.getLogger(__name__)


def on_clear_click() -> None:
    logger.debug("on_clear_click")
    del st.session_state[config.USER_MESSAGE][:]
    del st.session_state[config.BOT_MESSAGE][:]
    del st.session_state[config.HISTORY][:]
    st.session_state.chat_id = uuid.uuid4().hex


def on_table_change() -> None:
    logger.debug("on_save_click")
    db = Database()
    db.update_schema(st.session_state["chosen_tables"])
    logger.debug(f"Tables updated: {db.schema}")


def on_regen_click() -> None:
    logger.debug("on_regen_click")
    st.session_state[config.BOT_MESSAGE].pop()
    st.session_state.history.pop()
    st.session_state[config.USER_MESSAGE].pop()
    st.session_state.history.pop()


def on_lang_change() -> None:
    logger.debug("on_lang_change")
    on_clear_click()


def update_session_state_on_response(response: Message, update=False) -> None:
    logger.info("Updating session state on response")
    logger.debug(f"Response payload: {response}")
    if update:
        st.session_state[config.BOT_MESSAGE].pop()
        st.session_state.history.pop()

    st.session_state[config.BOT_MESSAGE].append(response)
    record = {"type": "AI"}
    if response.payload.text:
        record["text"] = response.payload.text
    if response.payload.code:
        record["code"] = response.payload.code
    if response.payload.df is not None:
        record["df"] = response.payload.df
    if response.payload.active is None:
        record["active"] = True

    st.session_state.history.append(record)
    logger.debug("Updating session state on response - done")
