from yandex_cloud_ml_sdk import YCloudML
import os 
from dotenv import load_dotenv
from sqlalchemy import inspect
#from db.connection import engine

load_dotenv()
#inspector = inspect(engine)
#tables = inspector.get_table_names()
tables =['user','agent','green']
columns = [
    "Год (integer)",
    "Спутник (string)",
    "Площадь с растительностью, кв. м (float)",
    "Площадь без растительности, кв. м (float)",
    "%A (float)",
    "1 - %A (float)",
    "%B (float)",
    "1 - %B (float)"
]
text = (
    f"В базе данных есть таблицы: {', '.join(tables)}.\n\n"
    f"Эти таблицы содержит следующие колонки: {', '.join(columns)}."
)
sdk = YCloudML(folder_id = os.getenv('FOLDER_ID'), auth= os.getenv('TOKEN'))
model = sdk.models.completions("yandexgpt")
prompt = f"""
Ты — генератор SQL для PostgreSQL.
Пиши только запрос без пояснений.
Экранируй имена столбцов двойными кавычками.
Ограничивай результат 100 строками.

Структура таблицы: 
{text}
"""
response = model.run(prompt)
print(response.text)