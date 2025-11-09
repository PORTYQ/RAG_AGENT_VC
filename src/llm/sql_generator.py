from yandex_cloud_ml_sdk import YCloudML
import os 
from dotenv import load_dotenv
from sqlalchemy import inspect
import re
#from src.db.connection import engine

def generate_sql_promt(engine,system_promt,request_user):
    load_dotenv()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    columns = [
        'id (integer)'
        "Год (integer)",
        "Спутник (string)",
        "Площадь с растительностью, кв. м (String)",
        "Площадь без растительности, кв. м (String)",
        "%A (String)",
        "1 - %A (String)",
        "%B (String)",
        "1 - %B (String)"
    ]
    text = (
        f"В базе данных есть таблицы: {', '.join(tables)}.\n\n"
        f"Эти таблицы содержит следующие колонки: {', '.join(columns)}."
    )
    sdk = YCloudML(folder_id = os.getenv('FOLDER_ID'), auth= os.getenv('TOKEN'))
    model = sdk.models.completions("yandexgpt")
    prompt = system_promt.format(
        text = text,
        request_user = request_user
    )
    #SQL запрос LLM
    response = model.run(prompt)
    sql_text = response.alternatives[0].text
    sql_text = re.sub(r"^```[a-zA-Z]*\n", "",sql_text)
    sql_text = re.sub(r"```$", "", sql_text)
    return sql_text
if __name__ == '__main__':
    pass