from src.db.connection import engine
from src.llm.sql_generator import generate_sql_promt
from src.prompts.loader import load_promt
from src.db.repository import fetch_to_df
from langchain_core.tools import tool

@tool
def run_sql_query(request_user:str,egine:str)->str:
    """
    Используй этот инструмент, когда пользователю нужно получить данные из базы,
    выполнить SQL-запрос, сгенерировать выборку или получить любую информацию,
    связанную с таблицами, датами, фильтрами, агрегатами или отчётами.

    Аргумент `request_user` — это формулировка задачи пользователя
    (например: "покажи продажи за 2021", "получи список клиентов",
    "вытащи данные по заказам за март").

    Инструмент должен получать на вход текстовое описание задачи и возвращать
    готовый SQL-запрос или результат его выполнения.
    """
    #Получение нужного промта
    system_promt = load_promt('sql_generator.txt')
    #Запрос пользователя
    sql_query = generate_sql_promt(engine,system_promt,request_user)
    result = fetch_to_df(sql_query,engine)
    return result

if __name__ == '__main__':
    pass