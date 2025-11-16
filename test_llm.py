from typing import Sequence, Any

from langchain_core.tools import BaseTool
from langchain.agents import create_react_agent
from langchain_core.runnables import RunnableConfig
from langchain_core.language_models import LanguageModelLike

import uuid
import os
from dotenv import find_dotenv, load_dotenv

from src.agents.tools.sql_tools import run_sql_query
from src.prompts.loader import load_promt
from langchain_gigachat import GigaChat  # <--- новый импорт

ModelT = str | LanguageModelLike

load_dotenv(find_dotenv())


class LLM:
    def __init__(self, model: ModelT, tools: Sequence[BaseTool]) -> None:
        self.model = model

        # Создаем агента (пока без чекпоинтера, чтобы не ловить thread_id ошибки)
        self._agent: Any = create_react_agent(
            model,
            tools,
        )

        # Конфиг можно оставить пустым или вообще не использовать
        self._config: RunnableConfig = {
            "configurable": {
                "thread_id": uuid.uuid4().hex
            }
        }

    def invoke(
        self,
        content: str,
        attachments: list[str] | None = None,
        temperature: float = 0.1,
    ) -> str:
        message: dict[str, Any] = {
            "role": "user",
            "content": content,
            **({"attachments": attachments} if attachments else {}),
        }

        result = self._agent.invoke(
            {
                "messages": [message],
                "temperature": temperature,
            },
            config=self._config,
        )

        # В состоянии у агента список messages
        return result["messages"][-1].content


def print_agent_response(llm_response: str) -> None:
    print(f"\033[31m{llm_response}\033[0m")


def get_user_prompt() -> str:
    return input("\nЗапрос: ")


def start_llm() -> None:
    #token = os.getenv("MDE5YTAxOWYtNzcxZS03OWIxLTlmOGEtNzhkNTMwYmZhMjVlOjQ2MDZhM2Q1LWY2ZTItNDJkOS1hNTZjLTY2MzQwZjc4MzhjMw==")
    # if token is None:
    #     raise ValueError("Переменная GIGACHAT_TOKEN не задана")

    model = GigaChat(
        model="GigaChat-2-Max",  # или "GigaChat-Pro", если только она доступна
        credentials='MDE5YTAxOWYtNzcxZS03OWIxLTlmOGEtNzhkNTMwYmZhMjVlOjQ2MDZhM2Q1LWY2ZTItNDJkOS1hNTZjLTY2MzQwZjc4MzhjMw==',
        scope="GIGACHAT_API_PERS",
        verify_ssl_certs=False,
    )

    agent = LLM(model, tools=[run_sql_query])
    system_prompt = load_promt("report_prompt.txt")

    # Первый ответ — по системному промту (можно убрать, если не нужно)
    agent_response = agent.invoke(content=system_prompt)

    while True:
        print_agent_response(agent_response)
        user_prompt = get_user_prompt()
        agent_response = agent.invoke(user_prompt)


if __name__ == "__main__":
    try:
        start_llm()
    except KeyboardInterrupt:
        print("\nЗавершение")
