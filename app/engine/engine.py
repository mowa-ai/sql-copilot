from typing import List

import pandas as pd

from app.engine.llm_chain import QueryChain
from app.engine.sql_engine import Database


def generate_query(text: str, history: List = None, lang: str = "English") -> str:
    db = Database()
    chain = QueryChain(db.schema, lang=lang)
    output = chain.generate_query(text, history=history)
    return output


def execute_query(query: str) -> pd.DataFrame:
    db = Database()
    output = db.execute_query(query=query)
    return output
