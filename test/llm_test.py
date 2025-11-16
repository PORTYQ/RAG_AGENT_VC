# Импортирование необходимой функциональности
from langchain_gigachat.chat_models import GigaChat
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Создание агента \{#sozdanie-agenta2}

memory = MemorySaver()
model = GigaChat(
    credentials="MDE5YTAxOWYtNzcxZS03OWIxLTlmOGEtNzhkNTMwYmZhMjVlOjQ2MDZhM2Q1LWY2ZTItNDJkOS1hNTZjLTY2MzQwZjc4MzhjMw==",
    scope="GIGACHAT_API_PERS",
    model="GigaChat-Pro",
    verify_ssl_certs=False,
)
search = TavilySearchResults(max_results=2)
tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Использование агента
config = {"configurable": {"thread_id": "abc100"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="Привет! Меня зову Вася. Я живу в Москве")]},
    config,
):
    print(chunk)
    print("----")

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="Узнай погоду в моем городе")]}, config
):
    print(chunk)
    print("----")