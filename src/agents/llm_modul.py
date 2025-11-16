from langchain_core.tools import BaseTool
from typing import Sequence,Any
from langgraph.prebuilt import create_react_agent
#from langgraph.checkpoint.memory import MemorySaver
#from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
import uuid
from langchain_core.language_models import LanguageModelLike
#from langchain_community.chat_models.yandex import ChatYandexGPT
import os
from dotenv import  load_dotenv
#from pydantic import SecretStr
from .tools.sql_tools import run_sql_query
from src.prompts.loader import load_promt
#from langchain_community.chat_models.gigachat import GigaChat
from langchain_gigachat.chat_models import GigaChat
ModelT = str | LanguageModelLike

load_dotenv()

class LLM:
    def __init__(self,model:ModelT,tools:Sequence[BaseTool]) -> None:
        self.model = model 

        #Создаем агента 
        self._agent:Any=create_react_agent(
            model=model,
            tools=tools,
            checkpointer=InMemorySaver()

        )
        self._config:RunnableConfig = {
            'configurable':{'thread_id':uuid.uuid4().hex}

        }
    def invoke(self,content:str,attachments:list[str]|None = None,temperature:float = 0.1) -> str :
            message:dict[str,Any] ={
                'role':'user',
                'content':content,
                **({'attachments':attachments} if attachments else {})
            }
            return self._agent.invoke({
                'messages':[message],
                'temperature':temperature,
            },
            config = self._config
            )['messages'][-1].content

def print_agent_response(llm_response: str) -> None:
     print(f'\033[31m{llm_response}\033[0m')

def get_user_prompt() -> str:
     return input('\nЗапрос:')

def start_llm():
     token = os.getenv("TOKEN")
     id_env = os.getenv('FOLDER_ID')
     if token is None:
          raise ValueError('Переменная TOKEN не задана')
     if id_env is None:
          raise ValueError('FOLDER_ID не задан')
     
     model = GigaChat(
          model="GigaChat-Pro",
          credentials =os.getenv('CREDENTIALS'),
          scope = os.getenv('SCOPE'),
          verify_ssl_certs=False,
     )
     agent = LLM(model,tools=[run_sql_query])
     system_prompt = load_promt('report_prompt.txt')
     agent_response = agent.invoke(content=system_prompt)

     while True:
          print_agent_response(agent_response)
          agent_response = agent.invoke(get_user_prompt())

if __name__ =='__main__':
     try:
          start_llm()
     except KeyboardInterrupt:
          print('\nЗавершение')          
