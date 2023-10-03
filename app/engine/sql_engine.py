import os
import sqlite3

import pandas as pd

PATH_TO_DATA = os.environ["PATH_TO_DATA"]


class Database(object):
    def __init__(self):
        self.con = sqlite3.connect(PATH_TO_DATA)
        self.tables = None
        self.schema, self.schema_dict = None, None
        self.update_schema()

    def execute_query(self, query: str) -> pd.DataFrame:
        df = pd.read_sql_query(query, self.con)
        return df

    def update_schema(self, chosen_tables=None) -> None:
        sql = "SELECT name FROM sqlite_master WHERE type='table';"
        self.tables = chosen_tables or [x[0] for x in self.execute_query(sql).values]
        self.schema = ""
        self.schema_dict = {}
        for t in self.tables:
            cursor = self.con.execute("SELECT sql FROM sqlite_master WHERE name=?;", [t])
            sql = cursor.fetchone()[0]
            cursor.close()
            self.schema += f"{t}:\n" + sql + "\n\n"
            self.schema_dict[t] = pd.read_sql_query(f"PRAGMA table_info({t})", con=self.con)[["name", "type"]]
