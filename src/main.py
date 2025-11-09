#Точка входа 
from db.connection import engine
from llm.sql_generator import generate_sql_promt
from prompts.loader import load_promt
from db.repository import fetch_to_df

def main():
    system_promt = load_promt('sql_generator.txt')
    request_user = 'покажи данные за 2021'
    sql_query = generate_sql_promt(engine,system_promt,request_user)
    result = fetch_to_df(sql_query,engine)
    return result

if __name__ == '__main__':
    print(main())
