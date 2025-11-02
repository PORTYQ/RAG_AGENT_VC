from sqlalchemy import text
import pandas as pd
from connection import engine


def fetch_to_df(query: str):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return pd.DataFrame(result.fetchall(), columns=result.keys())
