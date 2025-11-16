from yandex_cloud_ml_sdk import YCloudML
import os 
from dotenv import load_dotenv
from sqlalchemy import inspect
import re
from src.db.schema_introspection import get_full_schema,get_descriptions
#from src.db.connection import engine

def generate_sql_promt(engine,system_promt,request_user):
    load_dotenv()
    schema = get_full_schema(engine)
    descriptions = get_descriptions(schema)
    schema_txt = '\n'.join(descriptions)
    sdk = YCloudML(folder_id = os.getenv('FOLDER_ID'), auth= os.getenv('TOKEN'))
    model = sdk.models.completions("yandexgpt")
    prompt = system_promt.format(
        schema_txt = schema_txt,
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