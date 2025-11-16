#Точка входа 
# from db.connection import engine
# from llm.sql_generator import generate_sql_promt
# from prompts.loader import load_promt
# from db.repository import fetch_to_df

# def main():
#     #Получение нужного промта
#     system_promt = load_promt('sql_generator.txt')
#     #Запрос пользователя
#     request_user = 'покажи данные за 2021'
#     sql_query = generate_sql_promt(engine,system_promt,request_user)
#     #result = fetch_to_df(sql_query,engine)
#     return sql_query #result

# if __name__ == '__main__':
#     print(main())
from src.agents.llm_modul import start_llm

try:
    start_llm()
except KeyboardInterrupt:
    print('\nЗавершение')

