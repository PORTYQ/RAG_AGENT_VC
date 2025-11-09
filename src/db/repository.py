from sqlalchemy import text
import pandas as pd


def fetch_to_df(query: str,engine):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return pd.DataFrame(result.fetchall(), columns=result.keys())

if __name__ == '__main__':
    pass